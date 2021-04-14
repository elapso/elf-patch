#!/usr/bin/env python3

import click
import lief
import pathlib

@click.command()
@click.argument("fin", type=click.Path(exists=True))
@click.argument("fout", type=click.Path())
@click.option("--rpath", "rpath", type=click.Path(exists=True, resolve_path=True), 
    help='rpath parameter of dynamic section'    
)
@click.option("--runpath", "runpath", type=click.Path(exists=True, resolve_path=True), 
    help='runpath parameter of dynamic section'    
)
@click.option('--interpreter', "ld", type=click.Path(exists=True, resolve_path=True),
    help='path to ELF-interpreter shared object' 
)
def cli(fin, fout, runpath, rpath, ld):
    click.echo(fin)
    click.echo(fout)
    click.echo(runpath)
    click.echo(rpath)
    click.echo(ld)

if __name__ == '__main__':
    cli()
