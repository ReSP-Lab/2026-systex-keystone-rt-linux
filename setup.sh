#!/bin/sh

echo "--- Submodule initialisation ---"

git submodule update --init --recursive --depth 1

# Symlink examples and fs overlays

echo "--- Linking keystone enclaves and overlays ---"

echo "removing existing path..."

rm -rf keystone-6.6/examples
rm -rf keystone-rt/examples
rm -rf keystone-6.6/overlays/keystone/fs
rm -rf keystone-rt/overlays/keystone/fs

echo "Linking new patch existing path..."

ln -s ../keystone-enclaves keystone-6.6/examples
ln -s ../keystone-enclaves keystone-rt/examples
ln -s ../../../keystone-fs keystone-6.6/overlays/keystone/fs
ln -s ../../../keystone-fs keystone-rt/overlays/keystone/fs

echo "Done"

