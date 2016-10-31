#include <QVariant>
#include <QObject>
#include <QDomDocument>
#include <QDebug>
#include "newvalue.h"

QDebug operator<<(QDebug dbg, const Bar &message)
{
    dbg << "what";
    return dbg;
}

QDebug operator<<(QDebug dbg, const Foo &message)
{
    dbg << "what";
    return dbg;
}


Foo::Foo()
{
    static int i = 0;
    handle_ = "$"+ QString::number(++i);
}

Foo::~Foo()
{

    qDebug()<<"//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\"deleting foo  ";
}

int helper()
{
    static int i = 0;
    return ++i;
}

Bar::Bar(const Bar & bdd):QObject(bdd.parent())
{
    int i = helper();
    handle_ = "$"+ QString::number(i);
}
Bar::~Bar()
{
    qDebug()<<"//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\" deleting bar ";
}

Bar::Bar(QObject *p):QObject(p)
{
    int i = helper();
    handle_ = "$"+ QString::number(i);
}

