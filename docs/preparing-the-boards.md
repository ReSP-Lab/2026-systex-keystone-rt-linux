# Preparing the board

This contains instrutions about how to boot the HiFive Unmatched Rev. B board with the system on a µSD card.

For more details about the board requirements (power, cooling, ...), see the Sifive ["Getting Started Guide"](https://sifive.cdn.prismic.io/sifive/Z5KCu5bqstJ99zIu_hifive-unmatched-revb-gsg-v1p6_EN.pdf)

## Flashing the image

If you are using the prebuilt image, you can find them under `prebuilt-images/`. You can extract the archive using:

```bash
tar -xzf prebuilt-images/hifive_unmatched64.tar.gz -C prebuilt-images
tar -xzf prebuilt-images/hifive_unmatched64_rt.tar.gz -C prebuilt-images
```

If you are building the image yourself, the images will be generated under `keystone-rt/(...)/buildroot.build/images/sdcard.img`.


You can flash them into an µSD card using the following command (adapte the `if=...` path to point to the correct `.img` file and `of=...` to point to the µSD card).

```bash
sudo dd if=prebuilt-images/hifive_unmatched64.img of=/path/to/sd/card bs=1M status=progress
```

## Hifive Unmatched 

To boot from the SD card, the physical boot mode DIP switches `MSEL[3:0]` need to be set to `0100`.

![alt text](/figures/MSEL.png)


## Connection to the boards

Once the µSD card is plugged in and the HiFive Unmatched board is powered up, you can either connect to it using SSH or via the serial connection of the board (using screen or minicom) with baudrate set at `115200`.

`sudo screen -L /path/to/dev 115200`

The root password is `sifive`.

See [docs/running-the-experiments.md](running-the-experiments.md) to run the experiments.