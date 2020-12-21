import sys
import markov
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":

    args = sys.argv

    if args[1] == 'p':
        speaker_a = args[2]
        speaker_b = args[3]
        unknown_speaker = args[4]
        k = args[5]
        runs = args[6]

        with open(speaker_a) as file:
            speaker_one_text = file.read()
        with open(speaker_b) as file:
            speaker_two_text = file.read()
        with open(unknown_speaker) as file:
            unknown_speaker_text = file.read()

        output_dict = {
            'Implementation': []
            ,'K': []
            ,'Run': []
            ,'Time': []
        }

        # Run markov models for both dict and hashtable based on runs given
        for state in range(0, 2):
            for i in range(1, int(k) + 1):
                for run in range(1, int(runs) + 1):
                    start = time.perf_counter()
                    output_tuple = markov.identify_speaker(speaker_one_text,
                                                           speaker_two_text,
                                                           unknown_speaker_text,
                                                           i, state)
                    end = time.perf_counter()
                    elapsed_time = float(f'{end - start:0.4f}')
                    implementation = 'Hashtable' if state == 1 else 'dict'

                    output_dict['Implementation'].append(implementation)
                    output_dict['K'].append(i)
                    output_dict['Run'].append(run)
                    output_dict['Time'].append(elapsed_time)

        # build dataframe
        pd_data = pd.DataFrame(data=output_dict)
        pd_data_average = pd_data.groupby(['Implementation', 'K']).mean()\
            .reset_index()

        # create seaborn plot
        sns.set(style="darkgrid")
        graph = sns.pointplot(x='K', y='Time', hue='Implementation',
                              linestyle='-', marker='o', data=pd_data_average)
        graph.set_title('Hashtable vs Python Dict')
        graph.set_ylabel(f'Average Time (Runs={runs})')
        graph.set_xlabel(f'K')

        plt.savefig('execution_graph.png')

    else:
        speaker_a = args[1]
        speaker_b = args[2]
        unknown_speaker = args[3]
        k = args[4]
        state = args[5]

        with open(speaker_a) as file:
            speaker_one_text = file.read()
        with open(speaker_b) as file:
            speaker_two_text = file.read()
        with open(unknown_speaker) as file:
            unknown_speaker_text = file.read()

        output_tuple = markov.identify_speaker(speaker_one_text,
                                               speaker_two_text,
                                               unknown_speaker_text, int(k),
                                               int(state))

        print(f'Speaker A: {output_tuple[0]}')
        print(f'Speaker B: {output_tuple[1]}')
        print()
        print(f'Conclusion: Speaker {output_tuple[2]} is most likely')

