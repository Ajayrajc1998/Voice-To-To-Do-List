def recording_audio():
    import pyaudio
    import wave
    from pydub import AudioSegment
    # Set the audio format and other parameters
    audio_format = pyaudio.paInt16
    channels = 1
    sample_rate = 44100  # Adjust as needed
    chunk = 1024  # Adjust as needed
    seconds = 15# Adjust the recording duration as needed

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open a new audio stream for recording
    stream = audio.open(format=audio_format, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []
    for i in range(0, int(sample_rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    audio.terminate()

    # Save the recorded audio to a WAV file
    wav_output_file = "live_audio.wav"
    with wave.open(wav_output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    # Convert the WAV file to MP3 using pydub
    return wav_output_file


def audio_to_text():
    import assemblyai as aai
    import os
    # Replace with your API token
    aai.settings.api_key = os.environ.get("my_assemblyAI_Key")

    # Use the function to record and save audio as an MP3 file
    mp3_file = recording_audio()

    # You can also transcribe a local file by passing in a file path
    # FILE_URL = './path/to/file.mp3'

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(mp3_file)
    print(transcript.text)
    return transcript.text



def text_to_tasks(task_text):
    import openai
    from langchain.output_parsers import ResponseSchema
    from langchain.output_parsers import StructuredOutputParser
    import os
    from langchain.prompts import ChatPromptTemplate
    from langchain.chat_models import ChatOpenAI
    from langchain.output_parsers import ResponseSchema
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    print("text passed here and ready to get the results")
    output_template = """
    for the following text of various task extract the following information by finding the each task and assign the following for that each task, note that there is a high chance for b more than one task:
    timestamp: extract the time from the given text if no time mention take default time as 11 am instead make sure timestamp is there in every task
    completed: will be always False
    Task: extract the task from the given text and summarize it in a professional way to set a reminder if there is no text in input then only add You have a reminder! 
    level of importance: extract the level of importance and high, medium, low. if no level is mentioned set as medium
    task_id: assign a unique task ID
    format the output as JSON with the following keys:
    task_id
    timestamp
    completed
    Task
    level of importance
    text:{text}
    """
    timestamp_schema = ResponseSchema(name='timestamp', description="timestamp in the standard timestamp format YYYY-MM-DDTHH:MM:SS")
    completed_schema = ResponseSchema(name='completed', description='boolean value by default always False')
    Task_schema = ResponseSchema(name='Task', description='The task which is to be done')
    level_of_importance_schema = ResponseSchema(name='level of importance', description='three levels: high, medium, low; by default medium is set')
    task_id_schema = ResponseSchema(name='task_id', description='a unique task identifier')
    response_schemas = [timestamp_schema, completed_schema, Task_schema, level_of_importance_schema, task_id_schema]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt_template = ChatPromptTemplate.from_template(output_template)
    messages = prompt_template.format_messages(text=task_text, format_instructions=format_instructions)
    chat = ChatOpenAI(temperature=0.0, model='gpt-3.5-turbo')
    response = chat(messages)
    #output_dict = output_parser.parse(response.content)
    #task_list = task_text.split(".")  # Split the input text into individual tasks
    # task_list = [task.strip() for task in task_list if task.strip()]  # Remove empty tasks
    
    # tasks_output = []  # List to store the output for each task
    
    # for task_id, task_text in enumerate(task_list, start=1):
    #     messages = prompt_template.format_messages(text=task_text, format_instructions=format_instructions)
    #     chat = ChatOpenAI(temperature=0.0, model='gpt-3.5-turbo')
    #     response = chat(messages)
    #     output_dict = output_parser.parse(response.content)
    #     output_dict['task_id'] = task_id  # Add task_id to the output
    #     tasks_output.append(output_dict)
    
    return response.content

