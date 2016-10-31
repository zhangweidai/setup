
#ifndef NEWVALUE_H
#define NEWVALUE_H

#include <QVariant>
#include <QStringList>
#include <QObject>
#include <QDomDocument>
#include <QDebug>

class Newvalue : public QObject
{
    Q_OBJECT

public:
    bool hasHandle() const;

    void setHandle(const QString & key);

    QString variantToString(const QVariant & key) const;

    Newvalue(const QString & key);
    Newvalue(const QVariant & key, const Newvalue & value);
    Newvalue(const QVariant & key, const QVariant & value);
    Newvalue(const char * key, const QVariant & value);
    Newvalue(const QString & key, const QVariant & value);
    Newvalue(QObject *p = NULL);
    Newvalue(const Newvalue & rhs);

    ~Newvalue();

public:
    QString handle() const;
    QVariant key();
    QVariant value();

    void exportXml(QDomDocument* doc, QDomElement* element) const;
    void importXml(QDomDocument* doc, QDomElement* element) const;

public slots:

        //tran.set(m);
    void set(const QVariant & val);
    void set(const Newvalue & val);

    //tran.set("myparam", param);
    void set(const QVariant & key, const Newvalue & val);

    //param.get("vdd");
    QVariant get(const QVariant & key);

    QVariant get(const QVariantList & key);

    //param.set("vdd", 2);
    void set(const QVariant & key, const QVariant & val);

private:
    QVariant thisValue_;
    QVector<Newvalue*> valList_;
    QVariant val_;
    const Newvalue * nval_ = NULL;
    QString handle_;
};

Q_DECLARE_METATYPE(Newvalue)
Q_DECLARE_METATYPE(Newvalue*)

#endif
