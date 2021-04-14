#!/usr/bin/env python3

import click
import lief
import pathlib


@click.command(
    help="Change the interpreter, runpath and rpath of an ELF binary."
)
@click.argument("bin", type=click.Path(exists=True))
@click.options("--rpath", "rpath", type=click.Path(exists=True, resolve_path=True), 
    help='rpath parameter of dynamic section'    
)
@click.options("--runpath", "runpath", type=click.Path(exists=True, resolve_path=True), 
    help='runpath parameter of dynamic section'    
)
@click.options('--interpreter', "ld", type=click.Path(exists=True, resolve_path=True)
    help='path to ELF-interpreter shared object' 
)
@click.argument("out", type=click.Path())
def cli(bin, libc, ld, out):
    binary = lief.parse(bin)

    libc_name = None
    for i in binary.libraries:
        if "libc.so.6" in i:
            libc_name = i
            break

    if libc_name is None:
        click.echo("No libc linked. Exiting.")

    click.echo("Current ld.so:")
    click.echo("Path: {}".format(binary.interpreter))
    click.echo()

    libc_path = str(pathlib.Path(str(libc)).parent)

    binary.interpreter = str(ld)
    click.echo("New ld.so:")
    click.echo("Path: {}".format(binary.interpreter))
    click.echo()

    if binary.has(lief.ELF.DYNAMIC_TAGS.RPATH):
        click.echo ("Original rpath: {}".format(str(binary.get(lief.ELF.DYNAMIC_TAGS.RPATH))))
        binary.remove(lief.ELF.DYNAMIC_TAGS.RPATH)
        click.echo('has been removed')


    binary += lief.ELF.DynamicEntryRpath(libc_path)
    click.echo("Adding RPATH:")
    click.echo("Path: {}".format(libc_path))
    click.echo()

    binary += lief.ELF.DynamicEntryRunPath('./')
    click.echo("Adding RUNPATH: './'")
    click.echo("Path: {}".format(str(binary.get(lief.ELF.DYNAMIC_TAGS.RUNPATH))))
    click.echo()


    click.echo("Writing new binary {}".format(out))
    click.echo("Please rename {} to {}/libc.so.6.".format(
        libc, libc_path
    ))
    binary.write(out)


if __name__ == "__main__":
    cli()
