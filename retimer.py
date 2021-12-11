import datetime


def retime(frames, fps=60):
    total_seconds = frames / fps
    timedelta_obj = datetime.timedelta(seconds=total_seconds)
    return str(timedelta_obj)


if __name__ == "__main__":
    start_frame = 534-54
    end_frame = 198759-5
    print(retime(end_frame-start_frame))