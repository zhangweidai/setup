QT += core
QT += xml
QT += testlib
QT -= gui

QMAKE_CXXFLAGS += -std=c++11
QMAKE_CXXFLAGS += -Wno-unused-parameter

TARGET = untitled
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cc
SOURCES += newvalue.cc
HEADERS += newvalue.h
