#include <QCoreApplication>
#include <QDebug>
#include <QFileInfo>
#include <QStringList>
#include <QObject>
#include <QMetaType>
#include <QString>
#include <QDomDocument>
#include <iostream>


#include <boost/utility.hpp>
#include <boost/format.hpp>
#include <iostream>
#include <string>
#include <QVariant>
#include <QTest>
#include <boost/variant.hpp>

#include "newvalue.h"

using namespace std;


void test(const QVariant & well, const QVariant & again)
{
   QCOMPARE(well, again);
}


int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    qRegisterMetaType<Foo>("Foo");

    Foo foo;
    QVariant ffoo;
    ffoo.setValue(foo);

    Bar * bar = new Bar(&a);

    QVariant fbar;
    fbar.setValue(bar);

    Foo foo2 = ffoo.value<Foo>();
    Bar * bar2 = fbar.value<Bar*>();

    bar->str();
    bar2->str();

    foo.str();
    foo2.str();


    // Create a document to write XML
    QDomDocument * document = new QDomDocument();
    QDomElement root = document->createElement("Analysis");

    QDomDocument * document2 = new QDomDocument();
    QDomElement root2 = document2->createElement("Analysis");

/*
    Newvalue param("Param");
    param.set("vdd", 2);

    Newvalue tran("Tran");
    tran.set("mystop", 2);
    tran.set("mybool", true);
    tran.set("mystart", "2u");

    QMap<QString, QVariant> m;
    m.insert("map1", "3u");
    m.insert("map2", "23u");
    m.insert("map3", "13u");

    tran.set(m);
    tran.set("mymm", m);

    Newvalue ac("Ac", m);

    QVariantList vals;
    vals << QString("str");
    vals << QVariant(1);
    vals << QVariant(true);
    tran.set("myvalues", vals);
    tran.set("myparam", param);

    auto mybool = tran.get("mybool");
    test(mybool, true);

    auto tranvalue = tran.get("mystop");
    test(tranvalue, 2);

    auto map1 = tran.get(QVariantList() << "mymm");
    test(map1, m);

    auto map1value = tran.get(QVariantList() << "mymm"  << "map1");
    test(map1value, "3u");

    tran.exportXml(document, &root);
    ac.exportXml(document, &root);
    param.exportXml(document, &root);

    // Adding the root element to the docuemnt
    document->appendChild(root);
    document2->appendChild(root2);
    qDebug()  << "\033[32m( "<<__FILE__<<"-"<<__LINE__<<"  document " << " \033[0m|\n" << document->toString() <<"|)";
    qDebug()  << "\033[32m( "<<__FILE__<<"-"<<__LINE__<<"  document " << " \033[0m|\n" << document2->toString() <<"|)";
    */

    // Writing to a file
//    QFile file2("/tmp/myXML.xml");
//    if(!file2.open(QIODevice::WriteOnly | QIODevice::Text))
//    {
//        qDebug() << "Open the file for writing failed";
//    }
//    else
//    {
//        QTextStream stream(&file2);
//        stream << document.toString();
//        qDebug()  << "\033[32m( "<<__FILE__<<"-"<<__LINE__<<"  document " << " \033[0m|" << document.toString() <<"|)";
//        file2.close();
//        qDebug() << "Writing is done";
//    }
//
//    QFile file("/tmp/myXLM.xml");
//    if(!file.open(QIODevice::WriteOnly | QIODevice::Text))
//    {
//        qDebug() << "Open the file for writing failed";
//    }
//    else
//    {
//        QTextStream stream(&file);
//        stream << document.toString();
//        qDebug()  << "\033[32m( "<<__FILE__<<"-"<<__LINE__<<"  document " << " \033[0m|" << document.toString() <<"|)";
//        file.close();
//        qDebug() << "Writing is done";
//    }

   return 0;
}
