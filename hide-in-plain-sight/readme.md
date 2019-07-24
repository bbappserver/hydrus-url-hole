## What is this?
This program will take a given file, encipher it using a provided file and then write it to the specified file.

It will be written in the following format

```
[size: u64 | crypt_data bytes[size]]
```
This means you can put it anywhere including writing it to a raw device or partition.

To an outside observer without the secret this would just look like garbled unallocated bytes.  Unlike archives that include encryption, this does not even resemble an encrypted archive format. Because the outermost layer is encrypted, it doesn't contain any header information that would give it away as an encrypted archive.

This uses a simple xor scheme in '''ECB mode'''.  I'm to lazy to make a better scheme, but feel free to open a PR.
https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation


In a real filesystem your disk actually looks like this

```
device [
    partiiton table,
    partition1,
    partition2,
    ...
]

partition[filesystem]

filesystem
[
    headers
    catalog
]

catalog
[
    [file_path,file_size,checksum etc]
]
```

Using this tool you can just stick this block of raw data like this

```
device
[
    [size: u64 | crypt_data bytes[size]]
]
```

Which is indistinguishable from a device that was erased using secure random. '''NOTE: ECB Scheme - Some smartass might insist that there is something encrypted using aporbabilistic analysis to show you might have an arhcive of some sort, but you still have reasonable plausible deniability.  If you use a  compressed archive format, this kind of analysis could only really be performed on the header anyway.'''

## About device files
When under a Linux or Unix system you can directly access a device connected t your computer.  If prompted to '''initialize a device when you connect one of your hidden archives choose NO''', your device is intentionally uninitialized.

Devices on the system are in the `/dev` directory.
A device wil show up with a name like
`/dev/sda1`
If it is partitioned the first partition would be
`/dev/sda1s1`
the second
`/dev/sda1s2`
etc.

To write directly to a partition, bypassing the filesystem you write directly to the partition file, to ignore the partition file and write to the device, write directly to the device file.

Note that doing this will of course corrupt any foilsystem that has been formatted in a partition or on the device.

For the most convincing scheme I would recomment partitioning the device with a single partition, but not formatting it for a filesystem.  Then writing to  it.  As this would resemble a partitioned volume, that you just happened to securely erase.

## Usage

```bash
#encrypt a file
python encrypt.py e in_file encrypted_file secret_file 

#decrypt a file
python encrypt.py d encrypted_file out_file secret_file
```

e.g.
```bash
python encrypt.py e archive.zip /dev/sda1 keyfile.bin

python encrypt.py d /dev/sda1 archive.zip keyfile.bin
```

You can use a truely random selection of bytes for your secret file, but you will need to keep track of this file in order to recover your data.

You could use a book cipher instead.  A book cipher takes a quotation of some text as the cipher, this way as long as you can get access to the quotation you don't need a fishy secret file hanging around, you just reconstruct the secret when you need it.

The secret is case sensitive so if using a book cipher make sure you quote it exactly, you might want to make it all one case and remove punctuation to make it easier to remember.

Always test with a small file that you can encrypt and decrypt using your secret.

Before any inspections if using a book cipher destroy the secret file.

## Preparing files to be hidden
You may only write one file at a time, to prepare many files for transport you should first put them into an archive of your choice, or several archives if you will need to split your dataset across several devices.

### Preparing an archive of an arbitrary size.
You can download tools for spliting and then concatenating files on your system.  A file that has been split into multiple parts must be concatenated in the same order, and for many archive formats will be unable to partially reconstruct the dataset, should you loose one of thesplit files.  The advantage of this shceme however is that you do not have to juggle files into directories, and then make perfectly sized archives.  You can just construct one large archive and then split it so it is in the correct sized pieces to copy to your devices.

```
[A long TAR.tar]

[A.tar.0][long.tar.1][TAR.tat.2]
```

## Decrypting large archives
This dumb script doesn't understand how to send things through stdout into a pipeline, so use named pipes.

Create a pipe and put an a unarchiving command reading the output.
Then run the decrypt dumping data into this pipe.

e.g.

```bash
# construct a pipeline
mkfifo apipe 

#read the end pipe in the background assumes you used the tar.gz compressiong scheme
tar -xzf apipe &

#start writing the parts to the pipe
python encrypt.py d /dev/sda1 apipe keyfile.bin
```
