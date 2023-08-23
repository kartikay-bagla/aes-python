# AES Encryption
This is my implementation of the AES algorithim. Mostly intended as a learning project. Definitely would not recommend using this in any kind of production scenario.

### Installation/Setup
Python >= 3.10 and poetry (can be installed with `pip install poetry`). The other dependencies will be installed by poetry.

### Running
`poetry run python main.py --help` to get all the arguments.


### Generate S-Box Mapping

The S-Box table was lifted from [wikipedia](https://en.wikipedia.org/wiki/Rijndael_S-box) and was used to generate the mapping.  
To generate the output, run `poetry run python generate_s_box/parse_s_box_table.py`. It will use `generate_s_box/s_box_table.html` and `generate_s_box/inverse_s_box_table.html`.  
