
#ifndef NEWVALUE_H
#define NEWVALUE_H

#include <QVariant>
#include <QStringList>
#include <QObject>
#include <QDomDocument>
#include <QDebug>

class NewValue : public QObject
{
    Q_OBJECT

public:
    bool hasHandle() const;

    void setHandle(const QString & key);

    QString variantToString(const QVariant & key) const;

    NewValue(const QString & key);
    NewValue(const QVariant & key, const NewValue & value);
    NewValue(const QVariant & key, const QVariant & value);
    NewValue(const char * key, const QVariant & value);
    NewValue(const QString & key, const QVariant & value);
    NewValue(QObject *p = NULL);
    NewValue(const NewValue & rhs);

    ~NewValue();

public:
    QString handle() const;
    QVariant key();
    QVariant value();

    void exportXml(QDomDocument* doc, QDomElement* element) const;
    void importXml(QDomDocument* doc, QDomElement* element) const;

public slots:

    //tran.set(m);
    void set(const QVariant & val);
    void set(const NewValue & val);

    //tran.set("myparam", param);
    void set(const QVariant & key, const NewValue & val);

    //param.get("vdd");
    QVariant get(const QVariant & key);

    QVariant get(const QVariantList & key);

    //param.set("vdd", 2);
    void set(const QVariant & key, const QVariant & val);

private:
    QVariant thisValue_;
    QVector<NewValue*> valList_;
    QVariant val_;
    QString handle_;
};

Q_DECLARE_METATYPE(NewValue)
Q_DECLARE_METATYPE(NewValue*)
Q_DECLARE_METATYPE(const NewValue*)

#endif
