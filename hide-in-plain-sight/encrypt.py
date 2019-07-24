#!/bin/env python

import os,sys
from itertools import cycle


BLOCK_SIZE=4096
key_block=bytearray(BLOCK_SIZE)


#Note we should convert the key block to integers, but we aren't
#Since this isn't C the compiler can't figure out that we wanted
#to operate on the block a word at a time
#python wil literally go a byte at a time since it's interpreted not compiled
#This will be roughly 8 times as slow.


def encipher(text_file,cipher_file):
    cipher_block = bytearray(4096)
    block = bytearray(4096)

    file_length_in_bytes = os.path.getsize("test.txt")
    header=file_length_in_bytes.to_bytes(8, byteorder='big', signed=False)
    with open(text_file, "rb") as archive_file:
        with open(cipher_file, "wb") as binary_file:

            #We write the length to the start since we will write raw data to 
            #our device later, and we won't have a filesystem containing length data
            binary_file.write(header)
            
            while True:
                read_count = archive_file.readinto(block)
                if read_count <1:
                    break
                for i in range(len(block)):
                    a=block[i]
                    k=key_block[i]
                    c= a^k
                    cipher_block[i]=c


                # Write text or bytes to the file
                written_count=binary_file.write(cipher_block[:read_count])

def decipher(cipher_file,plain_file):
    cipher_block = bytearray(4096)
    block = bytearray(4096)
    with open(cipher_file, "rb") as archive_file:
        with open(plain_file, "wb") as binary_file:

            #We write the length to the start since we will write raw data to 
            #our device later, and we won't have a filesystem containing length data
            buf = bytearray(8)
            archive_file.readinto(buf)
            length=int.from_bytes(buf, byteorder='big', signed=False)
            
            read_qty=0
            while read_qty<length:
                read_count = archive_file.readinto(block)
                read_qty+=read_count
                for i in range(len(block)):
                    a=block[i]
                    k=key_block[i]
                    c= a^k
                    cipher_block[i]=c


                # Write text or bytes to the file
                binary_file.write(cipher_block[:read_count])

command=sys.argv[1]
in_file=sys.argv[2]
out_file=sys.argv[3]
secret_file=sys.argv[4]

#Load secret
with open(secret_file, "rb") as binary_file:
    key_tmp= binary_file.read()
    for i in range(len(key_block)):
        j= i % len(key_tmp)
        key_block[i]= key_tmp[j]

if command == "e":
    encipher(in_file,out_file)
elif command == "d":
    decipher(in_file,out_file)       


# #TEST
# encipher("test.txt","ciphertext.txt")
# decipher("ciphertext.txt","plaintext.txt")    