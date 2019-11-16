# Chapter 6 - Data preparation and pipelines

## Ref

- `https://www.reddit.com/r/WeAreTheMusicMakers/comments/3anwu8/the_drum_percussion_midi_archive_800k/`
- `https://www.reddit.com/r/WeAreTheMusicMakers/comments/3ajwe4/the_largest_midi_collection_on_the_internet/`
- maestro dataset
    - https://arxiv.org/abs/1810.12247
    - https://magenta.tensorflow.org/maestro-wave2midi2wave
    - https://magenta.tensorflow.org/onsets-frames
    - https://arxiv.org/abs/1809.04281
       

## Primers

- primer/jazz-ride.mid https://musescore.com/user/7942286/scores/1906646
- primer/jazz-drum-basic.mid https://musescore.com/user/13700046/scores/4662816

### Output

- chapter_06_example_00.py
    ```
    Number of tracks: 116189, number of tracks in sample: 116189, number of results: 5979 (5.15%)
    Time:  4814.2588857
    ```
- chapter_06_example_01.py
    ```
    Number of tracks: 31034, number of tracks in sample: 31034, number of results: 31034 (100.00%)
    Most common artists: [('Panpipes', 102), ('The Cranberries', 73), ('Mariah Carey', 57), ('Abba', 56), ('Richard Clayderman', 55), ('Mariano Yanani', 52), ('Scott Joplin', 51), ('Céline Dion', 49), ('The Police', 49), ('Creedence Clearwater Revival', 49), ('Green Day', 49), ('Enya', 47), ('Madonna', 47), ('Floyd Cramer', 45), ('The Corrs', 43), ('Queen', 42), ('Electric Light Orchestra', 40), ('Michael Jackson', 40), ('Linkin Park', 39), ('Avril Lavigne', 37), ('Nightwish', 37), ('Britney Spears', 37), ('Ace Cannon', 36), ('Duran Duran', 36), ('Aerosmith', 35)]
    Time:  21.0088559
    ```
- chapter_06_example_02.py
    ```
    Number of tracks: 31034, number of tracks in sample: 31034, number of results: 27743 (89.40%)
    Most common tags (100): [('pop', 1743), ('rock', 1116), ('80s', 805), ('country', 799), ('classic rock', 646), ('soul', 438), ('trance', 438), ('dance', 409), ('oldies', 332), ('70s', 309), ('electronic', 307), ('female vocalists', 292), ('60s', 283), ('italian', 252), ('disco', 236), ('instrumental', 213), ('indie', 203), ('jazz', 187), ('cover', 169), ('house', 163), ('christmas', 161), ('soundtrack', 160), ('progressive rock', 150), ('french', 143), ('rnb', 128), ('90s', 117), ('spanish', 114), ('alternative', 110), ('classical', 95), ('new wave', 89), ('piano', 86), ('hard rock', 85), ('latin', 83), ('folk', 82), ('hip-hop', 80), ('alternative rock', 75), ('reggae', 71), ('chillout', 71), ('rap', 68), ('singer-songwriter', 67), ('funk', 65), ('new age', 64), ('motown', 60), ('punk rock', 59), ('schlager', 58), ('chanson francaise', 57), ('heavy metal', 57), ('grunge', 56), ('smooth jazz', 55), ('ragtime', 54), ('easy listening', 54), ('symphonic metal', 54), ('blues', 53), ('techno', 53), ('britpop', 49), ('christian', 44), ('electro', 44), ('punk', 44), ('metal', 44), ('eurodance', 44), ('deutsch', 42), ('black metal', 40), ('power metal', 38), ('soft rock', 37), ('industrial', 36), ('electronica', 32), ('celtic', 32), ('gothic metal', 32), ('love', 31), ('indie rock', 31), ('progressive trance', 31), ('50s', 29), ('thrash metal', 29), ('guitar virtuoso', 28), ('ambient', 28), ('psytrance', 27), ('acoustic', 27), ('italianigdchill', 26), ('progressive metal', 26), ('classic country', 25), ('classical guitar', 25), ('covers', 25), ('romantic', 24), ('swedish', 24), ('finnish', 24), ('german', 23), ('minimal', 23), ('musical', 23), ('party', 23), ('melodic death metal', 23), ('chill', 23), ('southern rock', 23), ('christian rock', 22), ('ska', 22), ('seen live', 22), ('industrial metal', 22), ('synthpop', 22), ('indie pop', 21), ('gothic rock', 21), ('comedy', 20)]
    Time:  2449.2179278999997
    ```
- chapter_06_example_03.py
    ```
    Number of tracks: 31034, number of tracks in sample: 31034, number of results: 27743 (89.40%)
    Number of results: 27743, number of matched tags: 3138 (11.31%)
    Time:  2442.8953505
    ```
- chapter_06_example_04.py
    ```
    Number of tracks: 31034, number of tracks in sample: 31034, number of results: 30730 (99.02%)
    Time:  897.8264283
    ```
- chapter_06_example_05.py
    ```
    # NO
    ```
- chapter_06_example_06.py
    ```
    # NO
    ```
- chapter_06_example_07.py
    ```
    Number of tracks: 31034, number of tracks in sample: 31034, number of results: 1096 (3.53%)
    Time:  2531.8980853999997
    ```
- chapter_06_example_08.py
    ```
    Number of tracks: 31034, number of tracks in sample: 31034, number of results: 1473 (4.75%)
    Time:  2582.0384953
    ```
