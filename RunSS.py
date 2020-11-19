"""
  RunSS.py : Run the LArCV semantic segmentation (UResNet-Lonely)
             and point proposal (PPN) networks on Supera input.
             Store the output in a file.

  Original author:  J. Wolcott <jwolcott@fnal.gov>
             Date:  November 2020
"""

import argparse
import numpy
import pandas
import sys
import yaml

import mlreco.main_funcs

def LoadConfig(filename, model_file, input_files, use_gpu=True):
	cfg = yaml.load(open(filename))

	cfg["iotool"]["dataset"]["data_keys"] = input_files
	cfg["trainval"]["gpus"] = "0" if use_gpu else ""
	cfg["trainval"]["model_path"] = model_file

	# pre-process configuration (checks + certain non-specified default settings)
	mlreco.main_funcs.process_config(cfg)

	return cfg

def ParseArgs():
	parser = argparse.ArgumentParser()

	parser.add_argument("--config_file", "-c", required=True,
	                    help="YAML base configuration that will be augmented with other arguments.")
	parser.add_argument("--model_file", "-m", required=True,
	                    help="Path to Torch stored model weights file.")
	parser.add_argument("--input_file", "-i", required=True, action="append", default=[],
	                    help="Processed LArCV input file(s) to reconstruct.")
	parser.add_argument("--output_file", "-o", required=True,
	                    help="Target file to write output to.")

	parser.add_argument("--use_gpu", default=True)

	return parser.parse_args()

if __name__ == "__main__":
	args = ParseArgs()

	cfg = LoadConfig(args.config_file,
	                 args.model_file,
	                 args.input_file,
	                 use_gpu=args.use_gpu)

	handlers = mlreco.main_funcs.prepare(cfg)
	key = next(iter(cfg["iotool"]["dataset"]["schema"]))

	print("Reconstructing...")
	data = {}
	output = {}
	evt_counter = 0
	n_evts = len(handlers.data_io) * cfg["iotool"]["batch_size"]
	# the handlers.data_io_iter is an endless cycler.  we want to stop when we've made it through the dataset once
	def cycle(data_io):
		for x in data_io:
			yield x
	it = iter(cycle(handlers.data_io))
	while True:
		try:
			d, o = handlers.trainer.forward(it)
		except StopIteration:
			break

		evt_counter += len(d[key])
		print("\rProcessed %d/%d" % (evt_counter, n_evts), "events...", end='')

		# print(d["input_data"])
		# print(d["segment_label"])

		# todo: for some reason there are usually fewer true hit labels than reco hits.
		#       this is very weird because the "reco" hits are just true energy deposits...
		unmatched_indices = [idx for idx in range(len(d["input_data"])) if len(d["input_data"][idx]) != len(d["segment_label"][idx])]
		if any(unmatched_indices):
			for idx in unmatched_indices:
#				print("fixing event idx", idx, ": input data length is", len(d["input_data"][idx]), " while segement_label is", len(d["segment_label"][idx]))
				segment_label = numpy.empty_like(d["input_data"][idx][:, 4])
				numpy.put(segment_label, numpy.where(numpy.isin(d["input_data"][idx][:, :3], d["segment_label"][idx][:, :3]).all(axis=1)), d["segment_label"][idx][:, 4])
#				print("old length:", len(d["segment_label"][idx]), "new length:", len(segment_label))
				d["segment_label"][idx] = numpy.copy(d["input_data"][idx])
				d["segment_label"][idx][:, 4] = segment_label

#		print(d["segment_label"])

		assert len(d["input_data"]) == len(o["segmentation"])
		assert len(d["input_data"]) == len(d["segment_label"])
		assert all(len(d["input_data"][idx]) == len(d["segment_label"][idx]) for idx in range(len(d["input_data"])))
		assert all(len(d["input_data"][idx]) == len(o["segmentation"][idx]) for idx in range(len(d["input_data"])))

		# these are all dicts of lists (each list has one entry per event)
		for this_batch, all_batches in (d, data), (o, output):
			for k in this_batch:
				if k not in all_batches:
					all_batches[k] = []
				all_batches[k] += this_batch[k]

		sys.stdout.flush()

	with open(args.output_file, "wb") as outf:
		numpy.savez(outf, raw_data=data, ss_output=output)
