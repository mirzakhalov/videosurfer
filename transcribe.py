
from google.cloud import speech_v1
import io

class Transcribe:
    def __init__(self):
        print("hello")
    

    def recognize(self,local_file_path, model):
        """
        Transcribe a short audio file using a specified transcription model

        Args:
        local_file_path Path to local audio file, e.g. /path/audio.wav
        model The transcription model to use, e.g. video, phone_call, default
        For a list of available transcription models, see:
        https://cloud.google.com/speech-to-text/docs/transcription-model#transcription_models
        """

        client = speech_v1.SpeechClient()

        # local_file_path = 'resources/hello.wav'
        # model = 'phone_call'

        # The language of the supplied audio
        language_code = "en-US"
        config = {"language_code": language_code}
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = { "content": content}
        print("starting...")
        response = client.recognize(config, audio)
        
        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
        
    def recognize_v2(self, path):
        #Transcribe speech from a video stored on GCS."""
        from google.cloud import videointelligence

        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

        config = videointelligence.types.SpeechTranscriptionConfig(
            language_code='en-US',
            enable_automatic_punctuation=True)
        video_context = videointelligence.types.VideoContext(
            speech_transcription_config=config)

        operation = video_client.annotate_video(
            path, features=features,
            video_context=video_context)

        print('\nProcessing video for speech transcription.')

        result = operation.result(timeout=600)

        # There is only one annotation_result since only
        # one video is processed.
        annotation_results = result.annotation_results[0]
        for speech_transcription in annotation_results.speech_transcriptions:

            # The number of alternatives for each transcription is limited by
            # SpeechTranscriptionConfig.max_alternatives.
            # Each alternative is a different possible transcription
            # and has its own confidence score.
            for alternative in speech_transcription.alternatives:
                print('Alternative level information:')

                print('Transcript: {}'.format(alternative.transcript))
                print('Confidence: {}\n'.format(alternative.confidence))

                print('Word level information:')
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    print('\t{}s - {}s: {}'.format(
                        start_time.seconds + start_time.nanos * 1e-9,
                        end_time.seconds + end_time.nanos * 1e-9,
                        word))