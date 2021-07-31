# Data Wrangling Challenge

This is to normalize data from [European Union Road Safety Facts and Figures](https://en.wikipedia.org/wiki/Road_safety_in_Europe) 
and export the required data into a csv format.

## Running
This is containerized with docker and has to be installed to run.

- **To run the script**

```shell
docker-compose up
```
This will output (and update) the files described under [Files of Interest](#files-of-interest).

- **To run tests**

```shell
docker-compose run --rm app pytest
```

- **To run test with coverage**

```shell
docker-compose run --rm app pytest --cov
```

## Files of Interest
- `raw.csv`
This is the raw data as extracted from the html table from the above link. That is before the required transformation

- `data.csv`
This is the product of transforming the above data to the required specifications
  
- `data_with_header.csv`
Just like the previous but with titles (headers).