
#ifndef NEWVALUE_H
#define NEWVALUE_H

#include <QVariant>
#include <QObject>
#include <QDomDocument>
#include <QDebug>



class Foo
{
public :
    Foo();
    ~Foo();
    void str()
    {
        qDebug()  << "\033[32m( "<<__FILE__<<"-"<<__LINE__<<"  handle_ " << " \033[0m|" << handle_ <<"|)";
    }
    QString handle_;
};
Q_DECLARE_METATYPE(Foo)
Q_DECLARE_METATYPE(Foo*)


class Bar : public QObject
{
    Q_OBJECT

public :
    void str()
    {
        qDebug()  << "\033[32m( "<<__FILE__<<"-"<<__LINE__<<"  handle_ " << " \033[0m|" << handle_ <<"|)";
    }
    Bar(QObject *p = NULL);
    Bar(const Bar & b);
    ~Bar();
    QString handle_;
};
Q_DECLARE_METATYPE(Bar)
Q_DECLARE_METATYPE(Bar*)


/*
class Newvalue
{
    QVariant thisValue_;

    bool hasHandle() const
    {
        return !handle_.isEmpty();
    }

    void setHandle(const QString & key)
    {
        static int i = 0;
        handle_ = key + "$"+ QString::number(++i);
    }

    QString variantToString(const QVariant & key) const
    {
        if (!key.toString().isEmpty())
            return key.toString();

        QStringList list = key.toStringList();
        return list.join(",");
    }

public:
    Newvalue(const QString & key)
    {
        setHandle(key);
        thisValue_.setValue(key);
    }

    Newvalue(const QVariant & key, const Newvalue & value)
    {
        thisValue_.setValue(key);
        nval_ = (&value);
    }

    Newvalue(const QVariant & key, const QVariant & value)
    {
        thisValue_.setValue(key);
        val_.setValue(value);
    }

    Newvalue(const char * key, const QVariant & value)
    {
        setHandle(key);
        thisValue_.setValue(QString::fromStdString(key));
        set(value);
    }

    Newvalue(const QString & key, const QVariant & value)
    {
        setHandle(key);
        thisValue_.setValue(key);
        val_.setValue(value);
    }
    Newvalue()
    {
        setHandle("void");
    }

public:
    QString handle() const
    {
        return handle_;
    }

    QVariant key()   { return thisValue_; }
    QVariant value() { return val_; }

    void exportXml(QDomDocument* doc, QDomElement* element) const
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
            p.exportXml(doc, &valElement);
    }
//       void exportXml2(QDomDocument* doc, QDomElement* element) const
//       {
//       if (nval_ != NULL)
//       {
//       element->setAttribute(toString(), nval_->handle());
//       }
//       else if (val_.isNull())
//       {
//       QDomElement valElement = doc->createElement(toString());
//       element->appendChild(valElement);
//       foreach (Newvalue p, valList_)
//       p.exportXml2(doc, &valElement);
//       valElement.setAttribute("handle", handle_);
//       }
//       else
//       {
//       element->setAttribute(toString(), variantToString(val_));
//       }
//       }

    void importXml(QDomDocument* doc, QDomElement* element) const
    {
        Q_UNUSED(doc);
        Q_UNUSED(element);
    }

    public slots:

        //tran.set(m);
        void set(const QVariant & val)
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

    void set(const Newvalue & val)
    {
        qDebug()<<"//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\" set zero ";
        nval_ = (&val);
        val_.setValue(QVariant());
    }

    //tran.set("myparam", param);
    void set(const QVariant & key, const Newvalue & val)
    {
        // if new 
        bool added = false;
        foreach (auto var, valList_)
        {
            if (var.key() == key)
            {
                var.set(val);
                added = true;
            }
        }

        if (!added)
        {
            Newvalue newvar (key, val);
            valList_ << newvar;
        }
    }


    //param.get("vdd");
    QVariant get(const QVariant & key)
    {
        foreach (auto item, valList_)
        {
            if (item.key() == key)
                return item.value();
        }
        return QVariant();
    }

    QVariant get(const QVariantList & key)
    {
        if (key.size() == 1)
            return get(key[0]);
        QVariantList test2 = key.mid(1);
        return get(test2);
    }


    //param.set("vdd", 2);
    void set(const QVariant & key, const QVariant & val)
    {
        auto mapval = val.toMap();
        if (mapval.size() > 0)
        {
            Newvalue newfromMap (key, mapval);
            valList_ << newfromMap;
            return;
        }

        // if new 
        bool added = false;
        foreach (auto var, valList_)
        {
            if (var.key() == key)
            {
                var.set(val);
                added = true;
            }
        }
        if (!added)
        {
            Newvalue newvar (key, val);
            valList_ << newvar;
        }
    }

    private:
    QVector<Newvalue> valList_;
    QVariant val_;
    const Newvalue * nval_ = NULL;
    QString handle_;
};


*/

QDebug operator<<(QDebug dbg, const Bar &message);
QDebug operator<<(QDebug dbg, const Foo &message);
#endif
