import os, cv2
from typing import Union, List, Dict

audio_codecs = {
    "mp3": "libmp3lame",
    "aac": "aac",
    "opus": "libopus",
    "ogg": "libvorbis",
    "wav": "pcm_s16le",
    "flac": "flac",
    "alac": "alac",
    "ac3": "ac3",
    "eac3": "eac3",
    "wma": "wmav2",
    "amr-nb": "libopencore_amrnb",
    "amr-wb": "libopencore_amrwb",
    "dts": "dca",
    "g722": "g722",
    "g711": "pcm_alaw",
    "truehd": "mlp",
    "adpcm": "adpcm_ms",
    "mp2": "mp2",
    "speex": "libspeex",
}