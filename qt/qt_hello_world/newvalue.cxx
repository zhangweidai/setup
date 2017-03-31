#include <QVariant>
#include <QObject>
#include <QDomDocument>
#include <QDebug>
#include "newvalue.h"

bool NewValue::hasHandle() const
{
    return !handle_.isEmpty();
}

void NewValue::setHandle(const QString & key)
{
    static int i = 0;
    handle_ = key + "$"+ QString::number(++i);
}

QString NewValue::variantToString(const QVariant & key) const
{
    if (!key.toString().isEmpty())
        return key.toString();

    QStringList list = key.toStringList();
    return list.join(",");
}

NewValue::NewValue(const QString & key)
{
    setHandle(key);
    thisValue_.setValue(key);
}

NewValue::NewValue(const QVariant & key, const NewValue & value)
{
    thisValue_.setValue(key);
    const NewValue * p = & value;
    val_.setValue(p);
}

NewValue::NewValue(const QVariant & key, const QVariant & value)
{
    thisValue_.setValue(key);
    val_.setValue(value);
}

NewValue::NewValue(const char * key, const QVariant & value)
{
    setHandle(key);
    thisValue_.setValue(QString::fromStdString(key));
    set(value);
}

NewValue::NewValue(const QString & key, const QVariant & value)
{
    setHandle(key);
    thisValue_.setValue(key);
    val_.setValue(value);
}

NewValue::NewValue(QObject *p):QObject(p)
{
    setHandle("void");
}

NewValue::NewValue(const NewValue & rhs)
    :QObject(rhs.parent())
{
    valList_ = rhs.valList_;
    val_ = rhs.val_;
    handle_ = rhs.handle_;
    thisValue_ = rhs.thisValue_;
}

NewValue::~NewValue() { }

QString NewValue::handle() const
{
    return handle_;
}

QVariant NewValue::key()   { return thisValue_; }
QVariant NewValue::value() { return val_; }

void NewValue::exportXml(QDomDocument* doc, QDomElement* element) const
{
    QString label = (val_.isNull()) ? thisValue_.toString() : "field";
    if (val_.canConvert<NewValue*>())
    {
        QDomElement valElement = doc->createElement(label);
        element->appendChild(valElement);
        NewValue * nval = val_.value<NewValue*>();
        valElement.setAttribute(thisValue_.toString(), nval->handle());
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

void NewValue::importXml(QDomDocument* doc, QDomElement* element) const
{
    Q_UNUSED(doc);
    Q_UNUSED(element);
}

//tran.set(m);
void NewValue::set(const QVariant & val)
{
    auto mapval = val.toMap();
    if (mapval.size() > 0)
    {
        for (auto item = mapval.begin(); item != mapval.end(); ++item)
            set(item.key(), item.value());
        return;
    }

    val_.setValue(val);
}

void NewValue::set(const NewValue & val)
{
    qDebug()<<"//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\" set zero ";
    const NewValue * p = &val;
    val_.setValue(p);
}

//tran.set("myparam", param);
void NewValue::set(const QVariant & key, const NewValue & val)
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
        NewValue * newvar = new NewValue(key, val);
        valList_ << newvar;
    }
}


//param.get("vdd");
QVariant NewValue::get(const QVariant & key)
{
    foreach (auto item, valList_)
    {
        if (item->key() == key)
            return item->value();
    }
    return QVariant();
}

QVariant NewValue::get(const QVariantList & key)
{
    if (key.size() == 1)
        return get(key[0]);
    QVariantList test2 = key.mid(1);
    return get(test2);
}


//param.set("vdd", 2);
void NewValue::set(const QVariant & key, const QVariant & val)
{
    auto mapval = val.toMap();
    if (mapval.size() > 0)
    {
        NewValue * newfromMap = new NewValue(key, mapval);
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
        NewValue * newvar =  new NewValue(key, val);
        valList_ << newvar;
    }
}
