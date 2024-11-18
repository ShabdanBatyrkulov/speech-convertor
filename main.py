import sys
import torch
import asyncio

from recorder import Recorder
from speechbrain.inference.VAD import VAD
from models.speech_to_text import SpeechToTextModel
from models.text_to_text import TextToTextModel


async def main():
  # prepare
  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

  sample_rate = 16_000
  print(f'Sample rate: {sample_rate}')
  print("Please wait. Loading models...")
  print("INFO: Press CTRL+C to exit.")

  speech2text = SpeechToTextModel(device, sample_rate)
  text2text = TextToTextModel(device)

  record = Recorder(sample_rate)

  # start record/inference
  while True:
    t = await record()

    print("\nTranscribing your speech...")
    transcription, _, _ = speech2text(t)
    print('Transcription:', transcription, end='\n\n')

    print("Translating your speech...")
    translation, _, _ = text2text(transcription)
    print('Translation:', translation, end='\n\n')



if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    sys.exit('\nInterrupted by user')
