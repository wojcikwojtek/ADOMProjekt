import os
from multiprocessing import Pool, cpu_count
import soundfile as sf
import resampy

# funkcja do resamplingu
def resample_single_file(task):
    file_path, output_path, target_sr = task
    try:
        data, original_sr = sf.read(file_path)

        if original_sr == target_sr:
            sf.write(output_path, data, target_sr)
            return True

        # resampling
        resampled_data = resampy.resample(data, original_sr, target_sr, filter='kaiser_fast')
        sf.write(output_path, resampled_data, target_sr)
        return True
    except Exception as e:
        # raportowanie błędów
        return f"Error on {file_path}: {e}"


def batch_resample_parallel(input_dir, output_dir, target_sr=8000):
    print(f"Resampling do {target_sr} Hz")
    print(f"Skanowanie '{input_dir}' i tworzenie listy plików...")
    tasks = []

    # zebranie wszystkich plików .wav
    for root, dirs, files in os.walk(input_dir):
        wav_files = [f for f in files if f.lower().endswith('.wav')]
        if not wav_files:
            continue

        rel_path = os.path.relpath(root, input_dir)
        current_output_dir = os.path.join(output_dir, rel_path) if rel_path != "." else output_dir
        os.makedirs(current_output_dir, exist_ok=True)

        for filename in wav_files:
            file_path = os.path.join(root, filename)
            output_path = os.path.join(current_output_dir, filename)
            tasks.append((file_path, output_path, target_sr))

    total_files = len(tasks)
    print(f"Znaleziono {total_files} do resamplingu.")

    # 1 rdzeń mniej żeby nie zawiesić
    num_cores = max(1, cpu_count() - 1)
    print(f"Procesowanie z wykorzystaniem {num_cores} rdzeni CPU...\n")

    # dystrybucja na rdzenie
    processed_count = 0
    with Pool(processes=num_cores) as pool:
        for result in pool.imap_unordered(resample_single_file, tasks, chunksize=5):
            processed_count += 1

            if result is not True:
                print(f"\n{result}")

            if processed_count % 25 == 0 or processed_count == total_files:
                print(f"Progres: [{processed_count}/{total_files}] plików ukończonych...", end="\r")

    print(f"\n\n{processed_count} Zostało zresamplowanych,")

if __name__ == "__main__":
    # input folder - gdzie są pobrane pliki .wav
    input_root_folder = "./VCTK-Corpus"
    output_root_folder8k = "./VCTK-Corpus8k"
    output_root_folder4k = "./VCTK-Corpus4k"

    batch_resample_parallel(input_root_folder, output_root_folder8k, target_sr=8000)
    batch_resample_parallel(input_root_folder, output_root_folder4k, target_sr=4000)