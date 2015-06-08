# courtesy of https://github.com/babadofar/bbuzz_code/
mkdir vpdata
wget  http://www.vinmonopolet.no/api/produkter  -O vpdata/products.csv
iconv -f=ISO-8859-1 -t=UTF-8 vpdata/products.csv > vpdata/iconproducts.csv
rm vpdata/products.csv
