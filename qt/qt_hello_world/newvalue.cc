#include <QVariant>
#include <QObject>
#include <QDomDocument>
#include <QDebug>
#include "newvalue.h"

bool Newvalue::hasHandle() const
{
    return !handle_.isEmpty();
}

void Newvalue::setHandle(const QString & key)
{
    static int i = 0;
    handle_ = key + "$"+ QString::number(++i);
}

QString Newvalue::variantToString(const QVariant & key) const
{
    if (!key.toString().isEmpty())
        return key.toString();

    QStringList list = key.toStringList();
    return list.join(",");
}

Newvalue::Newvalue(const QString & key)
{
    setHandle(key);
    thisValue_.setValue(key);
}

Newvalue::Newvalue(const QVariant & key, const Newvalue & value)
{
    thisValue_.setValue(key);
    nval_ = (&value);
}

Newvalue::Newvalue(const QVariant & key, const QVariant & value)
{
    thisValue_.setValue(key);
    val_.setValue(value);
}

Newvalue::Newvalue(const char * key, const QVariant & value)
{
    setHandle(key);
    thisValue_.setValue(QString::fromStdString(key));
    set(value);
}

Newvalue::Newvalue(const QString & key, const QVariant & value)
{
    setHandle(key);
    thisValue_.setValue(key);
    val_.setValue(value);
}

Newvalue::Newvalue(QObject *p):QObject(p)
{
    setHandle("void");
}

Newvalue::Newvalue(const Newvalue & rhs)
    :QObject(rhs.parent())
{
    valList_ = rhs.valList_;
    val_ = rhs.val_;
    nval_ = rhs.nval_;
    handle_ = rhs.handle_;
    thisValue_ = rhs.thisValue_;
}

Newvalue::~Newvalue() { }

QString Newvalue::handle() const
{
    return handle_;
}

QVariant Newvalue::key()   { return thisValue_; }
QVariant Newvalue::value() { return val_; }

void Newvalue::exportXml(QDomDocument* doc, QDomElement* element) const
{
    QString label = (val_.isNull()) ? thisValue_.toString() : "field";
    if (nval_ != NULL)
    {
        QDomElement valElement = doc->createElement(label);
        element->appendChild(valElement);
        valElement.setAttribute(thisValue_.toString(), nval_->handle());
        return;
    }

    QDomElement valElement = doc->createElement(label);
    if (!val_.isNull())
    {
        auto mapval = val_.toMap();
        if (mapval.size() > 0)
        {
            QDomElement nodeElement = doc->createElement("hierarchy");
            element->appendChild(nodeElement);
            nodeElement.setAttribute("group", thisValue_.toString());

            for (auto item = mapval.begin(); item != mapval.end(); ++item)
            {
                QDomElement e1 = doc->createElement(label);
                nodeElement.appendChild(e1);
                e1.setAttribute(item.key(),  item.value().toString());
            }
        }
        else
        {
            element->appendChild(valElement);
            valElement.setAttribute(thisValue_.toString(), variantToString(val_));
        }
    }
    else
    {
        element->appendChild(valElement);
        valElement.setAttribute("handle", handle_);
    }

    foreach (auto p, valList_)
        p->exportXml(doc, &valElement);
}

void Newvalue::importXml(QDomDocument* doc, QDomElement* element) const
{
    Q_UNUSED(doc);
    Q_UNUSED(element);
}

//tran.set(m);
void Newvalue::set(const QVariant & val)
{
    auto mapval = val.toMap();
    if (mapval.size() > 0)
    {
        for (auto item = mapval.begin(); item != mapval.end(); ++item)
            set(item.key(), item.value());
        return;
    }

    val_.setValue(val);
    nval_ = NULL;
}

void Newvalue::set(const Newvalue & val)
{
    qDebug()<<"//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\" set zero ";
    nval_ = (&val);
    val_.setValue(QVariant());
}

//tran.set("myparam", param);
void Newvalue::set(const QVariant & key, const Newvalue & val)
{
    // if new 
    bool added = false;
    foreach (auto var, valList_)
    {
        if (var->key() == key)
        {
            var->set(val);
            added = true;
        }
    }

    if (!added)
    {
        Newvalue * newvar = new Newvalue(key, val);
        valList_ << newvar;
    }
}


//param.get("vdd");
QVariant Newvalue::get(const QVariant & key)
{
    foreach (auto item, valList_)
    {
        if (item->key() == key)
            return item->value();
    }
    return QVariant();
}

QVariant Newvalue::get(const QVariantList & key)
{
    if (key.size() == 1)
        return get(key[0]);
    QVariantList test2 = key.mid(1);
    return get(test2);
}


//param.set("vdd", 2);
void Newvalue::set(const QVariant & key, const QVariant & val)
{
    auto mapval = val.toMap();
    if (mapval.size() > 0)
    {
        Newvalue * newfromMap = new Newvalue(key, mapval);
        valList_ << newfromMap;
        return;
    }

    // if new 
    bool added = false;
    foreach (auto var, valList_)
    {
        if (var->key() == key)
        {
            var->set(val);
            added = true;
        }
    }
    if (!added)
    {
        Newvalue * newvar =  new Newvalue(key, val);
        valList_ << newvar;
    }
}
