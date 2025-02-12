import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
# from scipy.signal import fftconvolve

# prompt: オーディオのwavファイルを開いてサンプリングレートはそのままにして32bit floating のデータに変換して保存するソースコード。
def convert_to_32bit_float(input_wav, output_wav):
  """オーディオのwavファイルを開いてサンプリングレートはそのままにして
  32bit floating のデータに変換して保存する。

  Args:
    input_wav: 入力wavファイルのパス
    output_wav: 出力wavファイルのパス
  """

  try:
    fs, data = wavfile.read(input_wav)
  except FileNotFoundError:
    print(f"Error: The file '{input_wav}' was not found.")
    return False
  except ValueError:
    print(f"Error: The file '{input_wav}' is not a valid WAV file.")
    return False
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    return False

  data = deta_type_convert_to_32bit_float(data)

  try:
    wavfile.write(output_wav, fs, data)
  except PermissionError:
    print(f"Error: Permission denied when writing to '{output_wav}'.")
    return False
  except ValueError as e:
    print(f"Error: {e}")
    return False
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    return False

  return True
# 使用例
# input_wav_file = "input.wav"
# output_wav_file = "output.wav"
# convert_to_32bit_float(input_wav_file, output_wav_file)


#----------------------------------------------------------
# Data type Converter
#----------------------------------------------------------
def deta_type_convert_to_32bit_float(data):

  if data.dtype == np.int16:
    data = data.astype(np.float32) / 32768.0
  elif data.dtype == np.int32:
    data = data.astype(np.float32) / 2147483648.0
  elif data.dtype == np.int8:
    data = data.astype(np.float32) / 255.0
  elif data.dtype == np.float64:
    data = data.astype(np.float32)
  elif data.dtype == np.float32:
    pass
  elif data.dtype == np.uint8:
    data = data.astype(np.float32) / 255.0
  else:
    data = data.astype(np.float32)
    # D.C or Rise Error (T.B.D)

  return data


#----------------------------------------------------------
# simple convolver
#----------------------------------------------------------
def simple_convolver(input_wav_file, filter_wav_file, output_wav_file):
  # ファイルA (入力データ) を読み込む
  try:
    sample_rate, input_data = wavfile.read(input_wav_file)
    # print(input_data.dtype)
    input_data = deta_type_convert_to_32bit_float(input_data)
    # print(input_data.dtype)
  except Exception as e:
    raise Exception(f"Error opening input file {input_wav_file}: {e}")
    return False

  # ファイルB (フィルタ係数データ) を読み込む
  try:
    filter_sample_rate, filter_data = wavfile.read(filter_wav_file)
    # print(filter_data.dtype)
    filter_data = deta_type_convert_to_32bit_float(filter_data)
    # print(filter_data.dtype)
  except Exception as e:
    raise Exception(f"Error opening filter file {filter_wav_file}: {e}")
    return False

  # 入力データとフィルタデータがステレオであることを確認
  if input_data.ndim != 2 or input_data.shape[1] != 2:
    # print(f"Input data must be stereo (2 channels), but got {input_data.shape[1]} channels.")
    return False

  if filter_data.ndim != 2 or filter_data.shape[1] != 2:
    # print(f"Filter data must be stereo (2 channels), but got {filter_data.shape[1]} channels.")
    return False

  # デバッグ: フィルタデータの確認
  # print("Filter L Channel: min = ", np.min(filter_data[:, 0]), " max = ", np.max(filter_data[:, 0]))
  # print("Filter R Channel: min = ", np.min(filter_data[:, 1]), " max = ", np.max(filter_data[:, 1]))

  # print("Input L Channel: min = ", np.min(input_data[:, 0]), " max = ", np.max(input_data[:, 0]))
  # print("Input R Channel: min = ", np.min(input_data[:, 1]), " max = ", np.max(input_data[:, 1]))

  # LチャンネルとRチャンネルに対して個別にフィルタを適用
  # left_channel_filtered  = fftconvolve(input_data[:, 0], filter_data[:, 0], mode='same')
  left_channel_filtered = lfilter(filter_data[:,0], 1.0, input_data[:, 0])

  #right_channel_filtered = fftconvolve(input_data[:, 1], filter_data[:, 1], mode='same')
  right_channel_filtered = lfilter(filter_data[:, 1], 1.0, input_data[:, 1])

  # デバッグ: フィルタ後のデータの確認
  # print("Filtered L Channel: min = ", np.min(left_channel_filtered) , " max = ", np.max(left_channel_filtered))
  # print("Filtered R Channel: min = ", np.min(right_channel_filtered), " max = ", np.max(right_channel_filtered))

  # フィルタリングしたデータを結合してステレオ信号にする
  filtered_data = np.stack((left_channel_filtered, right_channel_filtered), axis=1)

  # 出力データを32bit float形式で保存する
  try:
    wavfile.write(output_wav_file, sample_rate, filtered_data.astype(np.float32))
  except Exception as e:
    raise Exception(f"Error writing output file {output_wav_file}: {e}")
    return False

  return True


#----------------------------------------------------------
# Main function
#
#  this version does not use device_file_name and meta_file_name.
#----------------------------------------------------------
def convert_personalize(raw_file_name, ear_file_name, device_file_name, meta_file_name, output_file_name):
  # Do Something
  # Simple Test
  # convert_to_32bit_float(raw_file_name, output_file_name)

  converted = simple_convolver(raw_file_name, ear_file_name, output_file_name)

  return converted



'''
# TBD
def prepare_data(raw_file_name, ear_file_name, device_file_name, meta_file_name):
  # T.B.D ...(not necessary?)

  return True
'''
