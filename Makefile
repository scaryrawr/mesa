# Makefile for source rpm: mesa
# $Id$
NAME := mesa
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
