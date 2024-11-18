import torch
import time
import asyncio
import sounddevice as sd
import numpy as np

from queue import Queue
from threading import Thread


async def record_buffer(buffer, sample_rate, **kwargs):
  loop = asyncio.get_event_loop()
  event = asyncio.Event()
  idx = 0

  def callback(indata, frame_count, time_info, status):
    nonlocal idx
    if status:
      print(status)
    remainder = len(buffer) - idx
    if remainder == 0:
      loop.call_soon_threadsafe(event.set)
      raise sd.CallbackStop
    indata = indata[:remainder]
    buffer[idx:idx + len(indata)] = indata
    idx += len(indata)

  stream = sd.InputStream(samplerate=sample_rate, callback=callback, dtype=buffer.dtype,
                          channels=buffer.shape[1], **kwargs)
  with stream:
    await event.wait()


async def play_buffer(buffer, sample_rate, **kwargs):
  loop = asyncio.get_event_loop()
  event = asyncio.Event()
  idx = 0

  def callback(outdata, frame_count, time_info, status):
    nonlocal idx
    if status:
      print(status)
    remainder = len(buffer) - idx
    if remainder == 0:
      loop.call_soon_threadsafe(event.set)
      raise sd.CallbackStop
    valid_frames = frame_count if remainder >= frame_count else remainder
    outdata[:valid_frames] = buffer[idx:idx + valid_frames]
    outdata[valid_frames:] = 0
    idx += valid_frames

  stream = sd.OutputStream(samplerate=sample_rate, callback=callback, dtype=buffer.dtype,
                           channels=buffer.shape[1], **kwargs)
  with stream:
    await event.wait()


class Recorder:
  def __init__(
      self,
      sample_rate: int
  ):
    self.sample_rate = sample_rate

  async def __call__(self):
    print('Starting...')
    # self.messages.put(True)

    buffer = np.empty((150_000, 1), dtype='float32')
    print("LOG_INFO:", "Start recording for ~10 seconds.\nPlease say something.")
    await record_buffer(buffer, self.sample_rate)
    print("LOG_INFO:", "Finished recording")

    print("LOG_INFO:", "Playing recording")
    await play_buffer(buffer, self.sample_rate)
    print("LOG_INFO:", "Finished playing recording")

    chunk = torch.from_numpy(buffer).squeeze()
    return chunk
