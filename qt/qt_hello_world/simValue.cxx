/* Copyright 2014 Mentor Graphics Corporation
    All Rights Reserved

 THIS WORK CONTAINS TRADE SECRET
 AND PROPRIETARY INFORMATION WHICH IS THE
 PROPERTY OF MENTOR GRAPHICS
 CORPORATION OR ITS LICENSORS AND IS
 SUBJECT TO LICENSE TERMS.
*/

#include "simValue.h"
#include "simUtils.h"

#include <boost/format.hpp>
#include <iostream>

#include "simDbg.h"
#include <sstream>
#include "simValueVisitor.h"
using boost::format;

#include <boost/utility.hpp>
#include "simSerializeOps.h"

using boost::next;
using namespace dbg;


namespace simdb
{

struct PyObjectVisitor : static_visitor<PyObject*> {
   // template<typename T>
   // PyObject* operator()(T value) const {
   //    PyObject *none = Py_None;
   //    Py_INCREF(none);
   //    return none;
   // }
   PyObject* operator()(Void value) const {
      PyObject *none = Py_None;
      Py_INCREF(none);
      return none;
   }

   PyObject* operator()(int value) const {
      return PyInt_FromLong((long)value);
   }
   PyObject* operator()(double value) const {
      return PyFloat_FromDouble(value);
   }
   PyObject* operator()(bool value) const {
      return PyBool_FromLong(value ? 1 : 0);
   }
   PyObject* operator()(QString& value) const {
       QString temp ((&value)->data());
      return PyString_FromStringAndSize(temp.toStdString().c_str(),(&value)->size());
   }
   PyObject* operator() (const ValVector& vec) const {
      PyObject *l;
      l = PyList_New(vec.size());
      for(size_t idx=0; idx < vec.size(); ++idx) {
         //*(vec[idx]);
         PyList_SetItem(l, idx, vec[idx]->get());
      }
      return l;
   }

   PyObject* operator() (const ValMap& val) const {
      PyObject* d;
      d = PyDict_New();
      ValMap::const_iterator vit;
      for(vit = val.begin(); vit != val.end(); ++vit) {
         PyDict_SetItem(d, PyString_FromString(vit->first.toStdString().c_str()), vit->second->get());
         //*(vit->second);
      }
      return d;
   }
   PyObject* operator() (const ValuePtr& valp) const {
      return valp->get();
   }

};

PyObject* Value::get()
{
   return boost::apply_visitor(PyObjectVisitor(), val_);
}

IMPLEMENT_SERIALIZABLE(Value, 1.0)
// Value
Value::Value(const Value& rhs) : QObject(), boost::enable_shared_from_this<Value>()
{
    val_ = rhs.val_;
}
Value& Value::operator=(const Value& rhs)
{
    if (&rhs != this )
        val_ = rhs.val_;

    return *this;
}


Value::Value()
    : val_(Void())
{
}
Value::Value(ValuePtr valp)
    : val_(valp->val_)
{
    //mgc__assert(false, "Constructor from ValuePtr discourged");
}
Value::Value(int val)
    : val_(val)
{
}
Value::Value(double val)
    : val_(val)
{
}
Value::Value(bool val)
    : val_(val)
{
}

//Value::Value(const QString & val)
//    : val_(val.toStdString())
//{
//}
Value::Value(const char *val)
    : val_(QString(val))
{
}
Value::Value(const QString& val)
    : val_(val)
{
}
Value::Value(const ValVector& val)
    : val_(val)
{
}
Value::Value(const BoolVec& bvec)
{
    set(bvec);
}
Value::Value(const IntVec& ivec)
{
    set(ivec);
}
Value::Value(const DoubleVec& dvec)
{
    set(dvec);
}
Value::Value(const StringVec& svec)
{
    set(svec);
}
Value::Value(const ValMap& valmap)
    : val_(valmap)
{
}

Value::~Value()
{
}

void Value::set(ValuePtr valp)
{
    // DBG_MSG(boost::str(boost::format("Value in Valptr") ));
    // valp->dump();
    //val_ = valp;
    val_ = valp->val_;
}

void Value::set(int val)
{
    val_ = val;
}
void Value::set(double val)
{
    val_ = val;
}
void Value::set(bool val)
{
    val_ = val;
}
void Value::set(const char* val)
{
    val_ = QString(val);
}
void Value::set(const QString& val)
{
    val_ = val;
}
void Value::set(const BoolVec& bvec)
{
    ValVector vec(bvec.size());
    BoolVec::const_iterator vit;

    for (size_t idx = 0; idx < bvec.size(); ++idx)
    {
        DBG_MSG(boost::str(boost::format("Bool Vec entry[%d] = %s") % idx % ( bvec[idx] ? "True" : "False") ));
        vec[idx] = ValuePtr(new Value(bvec[idx]));
    }

    val_ = vec;
}
void Value::set(const IntVec& ivec)
{
    ValVector vec(ivec.size());
    IntVec::const_iterator vit;

    for (size_t idx = 0; idx < ivec.size(); ++idx)
    {
        DBG_MSG(boost::str(boost::format("Int Vec entry[%d] = %d") % idx % ivec[idx]));
        vec[idx] = ValuePtr(new Value(ivec[idx]));
    }

    val_ = vec;
}
void Value::set(const DoubleVec& dvec)
{
    ValVector vec(dvec.size());
    DoubleVec::const_iterator vit;

    for (size_t idx = 0; idx < dvec.size(); ++idx)
    {
        DBG_MSG(boost::str(boost::format("Double Vec entry[%d] = %f") % idx % dvec[idx]));
        vec[idx] = ValuePtr(new Value(dvec[idx]));
    }

    val_ = vec;
}

void Value::set(const StringVec& svec)
{
    ValVector vec(svec.size());
    StringVec::const_iterator vit;

    for (size_t idx = 0; idx < svec.size(); ++idx)
    {
        DBG_MSG(boost::str(boost::format("Str Vec entry[%d] = %s") % idx % svec[idx]));
        vec[idx] = ValuePtr(new Value(svec[idx]));
    }

    val_ = vec;
}

void Value::set(const ValMap& valmap)
{
    ValMap::const_iterator vit;

    for (vit = valmap.begin(); vit != valmap.end(); ++vit)
    {
        ValuePtr valp = vit->second;
        DBG_MSG(boost::str(boost::format("**** Field name: %s") % vit->first ));
        valp->dump();
    }

    val_ = valmap;
}

void Value::remove(const QString& handle)
{
    // Better if we set status here
    if (!isVector())
        throw ValueTypeMismatch("append function failed, underlying type is not a vector");

    ValVector& vec = boost::get<ValVector>(val_);

    for (ValVector::iterator it = vec.begin(); it != vec.end(); ++it)
    {
        if ((*it)->formStr() == handle)
        {
            vec.erase(it);
            break;
        }
    }
}


void Value::append(ValuePtr val)
{
    if (isVoid())
        val_ = ValVector();

    // Better if we set status here
    if (!isVector())
        throw ValueTypeMismatch("append function failed, underlying type is not a vector");

    boost::get<ValVector>(val_).push_back(val);
}
void Value::append(int val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(double val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(bool val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const char* val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const QString& val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const BoolVec& val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const IntVec& val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const DoubleVec& val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const StringVec& val)
{
    append(ValuePtr(new Value(val)));
}
void Value::append(const ValMap& val)
{
    append(ValuePtr(new Value(val)));
}


ValuePtr Value::operator[](size_t idx)
{
    // Better if we set status here
    if (!isVector())
        throw ValueTypeMismatch("insert function failed, underlying type is not a vector");

    ValVector& valVec = boost::get<ValVector>(val_);

    if ( idx + 1 > valVec.size() )
        throw ValueVectorIdxOutOfBounds(QString("Vector idx: %1 out of bounds 0 - %2").arg(idx).arg(valVec.size()));
//                boost::str(boost::format(
//                            ));
//        throw ValueVectorIdxOutOfBounds(boost::str(boost::format("Vector idx: %d out of bounds 0 - %d") % idx % valVec.size()));

    return valVec[idx];
}

void Value::insert(const QString& key, ValuePtr val)
{
    if (isVoid())
        val_ = ValMap();

    // Better if we set status here
    if (!isMap())
        throw ValueTypeMismatch("insert function failed, underlying type is not a map");

    boost::get<ValMap>(val_).insert(std::make_pair(key, val));
}
void Value::insert(const QString& key, int val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, double val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, bool val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const char* val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const QString& val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const BoolVec& val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const IntVec& val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const DoubleVec& val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const StringVec& val)
{
    insert(key, ValuePtr(new Value(val)));
}
void Value::insert(const QString& key, const ValMap& val)
{
    insert(key, ValuePtr(new Value(val)));
}



ValuePtr Value::find(const QString& key)
{
    // Better if we set status here
    if (!isMap())
        throw ValueTypeMismatch("insert function failed, underlying type is not a map");

    ValMap& valMap = boost::get<ValMap>(val_);
    ValMap::iterator it = valMap.find(key);

    if (it != valMap.end())
        return it->second;

    return ValuePtr();
}

bool Value::getBool()
{
    return boost::apply_visitor(BoolVisitor(), val_);
}

int Value::getInt()
{
    return boost::apply_visitor(IntVisitor(), val_);
}
double Value::getDouble()
{
    return boost::apply_visitor(DoubleVisitor(), val_);
}
QString Value::getString()
{
    return boost::apply_visitor(StringVisitor(), val_);
}

ValuePtr Value::getValue()
{
    return ValuePtr(new Value(*this));
}

struct dumper : public boost::static_visitor<>
{
    int            nest_level_;
    std::ostream&  os_;
    dumper(int nestLevel, std::ostream& dumpOut )
        :
        nest_level_(nestLevel),
        os_(dumpOut)
    {}

    // template <typename T>
    //    void operator() (T& operand) const {
    //       os_ << operand << std::endl;
    //    }
    void operator() (Void val) const
    {
        indentDump(nest_level_ + 1, os_ ) << "void" << std::endl;
    }
    void operator() (const int val) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("int: %d") % val << std::endl;
    }
    void operator() (const double val) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("double: %f") % val << std::endl;
    }
    void operator() (const bool val) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("bool: %s") % (val ? "True" : "False" ) << std::endl;
    }
    void operator() (const QString& val) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("str: %s") % val << std::endl;
    }
    void operator() (const ValVector& vec) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("ValVector:")  << std::endl;

        for (size_t idx = 0; idx < vec.size(); ++idx)
        {
            indentDump(nest_level_ + 2, os_ ) << format("[%d] = ") % idx;
            boost::apply_visitor(dumper(nest_level_ + 2, os_), *(vec[idx]));
        }
    }

    void operator() (const ValMap& val) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("ValMap:")  << std::endl;
        ValMap::const_iterator vit;

        for (vit = val.begin(); vit != val.end(); ++vit)
        {
            indentDump(nest_level_ + 2, os_ ) << format("(%-15s) -> ") % vit->first;
            boost::apply_visitor(dumper(nest_level_ + 2, os_), *(vit->second));
        }
    }
    void operator() (const ValuePtr& valp) const
    {
        indentDump(nest_level_ + 1, os_ ) << format("ValuePtr:")  << std::endl;
        boost::apply_visitor(dumper(nest_level_ + 2, os_), *(valp));
    }


};

struct stringFormatter : public boost::static_visitor<QString>
{
    // template <typename T>
    //    void operator() (T& operand) const {
    //       os_ << operand << std::endl;
    //    }
    QString operator() (Void val) const
    {
        return "void";
    }
    QString operator() (const int val) const
    {
        return QString::number(val);
//        return boost::str(format("%d") % val);
    }
    QString operator() (const double val) const
    {
        return QString::number(val);
//        return boost::str(format("%f") % val);
    }
    QString operator() (const bool val) const
    {
        return (val ? "True" : "False");
//        return boost::str(format("%s") % (val ? "True" : "False"));
    }

    QString operator() (const QString& val) const
    {
        return val;
    }

    QString operator() (const ValVector& vec) const
    {
        QString str = "{";

        for (size_t idx = 0; idx < vec.size(); ++idx)
        {
            str += QString("[%1] -> %2").arg(idx).arg(vec[idx]->formStr());
//            str += boost::str(format("[%d] -> %s") % idx % vec[idx]->formStr());

            if (idx != vec.size() - 1 )
                str += ", ";
        }

        str += "}";
        return str;
    }

    QString operator() (const ValMap& val) const
    {
        QString str = "{";
        ValMap::const_iterator vit;

        for (vit = val.begin(); vit != val.end(); ++vit)
        {
            str += QString("(%1) -> %2").arg(vit->first).arg(vit->second->formStr());
//            str += boost::str(format("(%s) -> %s") % vit->first % vit->second->formStr());

            if (boost::next(vit) != val.end())
                str += ", ";
        }

        str += "}";
        return str;
    }
    QString operator() (const ValuePtr& valp) const
    {
        return valp->formStr();
    }


};
struct typeFormatter : public boost::static_visitor<QString>
{
    // template <typename T>
    //    void operator() (T& operand) const {
    //       os_ << operand << std::endl;
    //    }
    QString operator() (Void val) const
    {
        return "Void";
    }
    QString operator() (const int val) const
    {
        return "Int";
    }
    QString operator() (const double val) const
    {
        return "Double";
    }
    QString operator() (const bool val) const
    {
        return "Bool";
    }
    QString operator() (const QString& val) const
    {
        return "String";
    }
    QString operator() (const ValVector& vec) const
    {
        return "Vector";
    }
    QString operator() (const ValMap& val) const
    {
        return "Map";
    }
    QString operator() (const ValuePtr& valp) const
    {
        return "ValPointer";
    }
};


struct DstreamWriter : public boost::static_visitor<void>
{

    int            nest_level_;
    QDataStream&   ds_;
    DstreamWriter(int nestLevel, QDataStream& ds)
        :
        nest_level_(nestLevel),
        ds_(ds)
    {}

    // template <typename T>
    // void operator() (T& operand) const {
    //    ds_ << operand;
    // }
    void operator() (Void val) const
    {
        ds_ << val;
    }
    void operator() (const int val) const
    {
        ds_ << val;
    }
    void operator() (const double val) const
    {
        ds_ << val;
    }
    void operator() (const bool val) const
    {
        ds_ << val;
    }
    void operator() (const QString& val) const
    {
        ds_ << val;
    }
    void operator() (const ValVector& val) const
    {
        ds_ << val;
    }
    void operator() (const ValMap& val) const
    {
        operator<<(ds_, *(static_cast<const ValMap*>(&val)));
    }
    void operator() (const ValuePtr& val) const
    {
        operator<<(ds_, val);
    }


};


struct EqualOp : public boost::static_visitor<bool>
{

    template <typename T1, typename T2>
    bool operator() (const T1& lhs, const T2& rhs) const
    {
        return false;
    }
    bool operator() (const Void& lhs, const Void& rhs) const
    {
        return true;
    }
    bool operator() (const int lhs, const int rhs) const
    {
        return lhs == rhs;
    }
    bool operator() (const double lhs, const double rhs) const
    {
        return lhs == rhs;
    }
    bool operator() (const double lhs, const int rhs) const
    {
        return lhs == (double)rhs;
    }
    bool operator() (const int lhs, const double rhs) const
    {
        return (double)lhs == rhs;
    }
    bool operator() (const bool lhs, const bool rhs) const
    {
        return lhs == rhs;
    }
    bool operator() (const QString& lhs, const QString& rhs) const
    {
        return lhs == rhs;
    }
    bool operator() (const ValVector& lhs, const ValVector& rhs) const
    {
        if (lhs.size() != rhs.size())
            return false;

        for (size_t idx = 0; idx < lhs.size(); ++idx)
        {
            bool eq = boost::apply_visitor(EqualOp(), lhs[idx]->val_, rhs[idx]->val_);

            if (!eq)
                return false;
        }

        return true;
    }

    bool operator() (const ValMap& lhs, const ValMap& rhs) const
    {
        if (lhs.size() != rhs.size())
            return false;

        ValMap::const_iterator vit;

        for (vit = lhs.begin(); vit != lhs.end(); ++vit)
        {
            QString key = vit->first;
            //ValuePtr rhsVal = rhs.find(key);
            ValMap::const_iterator vit2 = rhs.find(key);

            if (vit2 == rhs.end())
                return false;

            ValuePtr lhsPtr = vit->second;
            ValuePtr rhsPtr = vit2->second;

            if (!lhsPtr && !rhsPtr)
                continue;

            if (!lhsPtr)
                return false;

            if (!rhsPtr)
                return false;

            bool eq = boost::apply_visitor(EqualOp(), lhsPtr->val_, rhsPtr->val_);

            if (!eq)
                return false;
        }

        return true;
    }
    bool operator() (const ValuePtr& lhs, const ValuePtr& rhs) const
    {
        return boost::apply_visitor(EqualOp(), lhs->val_, rhs->val_);
    }


};
bool Value::operator==(const Value& rhs) const
{
    return boost::apply_visitor(EqualOp(), val_, rhs.val_);
}

bool Value::operator!=(const Value& rhs) const
{
    return !operator==(rhs);
}

ValVector& Value::vector()
{
    if (!isVector())
        throw ValueTypeMismatch("vector function failed, underlying type is not a vector");

    ValVector& vec = boost::get<ValVector>(val_);
    return vec;
}
ValMap& Value::map()
{
    if (!isMap())
        throw ValueTypeMismatch("map function failed, underlying type is not a map");

    ValMap& map = boost::get<ValMap>(val_);
    return map;
}

//QString Value::toStr() const
//{
//    return (boost::apply_visitor(stringFormatter(), val_));
//}

QString Value::formStr() const
{
    return boost::apply_visitor(stringFormatter(), val_);
}
QString Value::typeName() const
{
    return boost::apply_visitor(typeFormatter(), val_);
}
SimSerializable* Value::createFromStream(QDataStream& ds, float version, Status& status)
{
    Value* objP = new Value();
    objP->read(ds, status);
    return objP;
}

void Value::write(Stream& ds, Status& status)
{
    DBDUMP( "Writing Value" );
    ds.writeField(FIELD__VAR_VALUE, val_);
    ds.writeEnd();
    DBDUMP( "Done Writing Value" );
}

void Value::write(QDataStream& ds, Status& status)
{
    DBDUMP( "Writing Value" );
    WRITE_FIELD(ds, FIELD__VAR_VALUE, val_);
    writeEnd(ds);
    DBDUMP( "Done Writing Value" );
}

void Value::read(QDataStream& ds, Status& status)
{
    DBDUMP( "Reading Value" );
    int tag;

    while ( ((tag = readTag(ds) ) != FIELD__END ) && (ds.status() == QDataStream::Ok ))
    {
        //DBDUMP(boost::str(boost::format("Loop: Value::read tag %s") % Value::SerFieldsStrs::inst().strs_[tag] ));
        switch (tag)
        {
        case FIELD__VAR_VALUE:
            val_ = READ_FIELD(VarVal, ds);
            break;

        default:
            skipField(ds);
        }
    }

    DBDUMP( "Done Reading Value" );
}

//PyObject* Value::getSWIGProxy() {
//   return targetPy::getSWIGProxy("simdb", "Value_getSWIGProxyS", shared_from_this());
//}

//ValuePtr Value::getSWIGProxyS(size_t address) {
//   return targetPy::getSWIGProxyS<Value>(address);
//}

//ValuePtr Value::fromPy(PyObject* obj)
//{
//   return targetPy::fromPyS<Value>(obj, "simdb");
//}

void Value::dump(
    const char *const nameP,    // pointer to object name
    const int         nestLevel,   // nesting level
    std::ostream& dumpOut
) const
{
    startDump("Value", this, nameP, nestLevel, dumpOut);
    //indentDump(nestLevel + 1, dumpOut ) << "" << std::endl;
    boost::apply_visitor(dumper(nestLevel, std::cout), val_);
    endDump(nestLevel, dumpOut);
}


ValuePtr value__void    = ValuePtr( new Value());
ValuePtr value__true    = ValuePtr( new Value(true));
ValuePtr value__false   = ValuePtr( new Value(false));
} // namespace simdb

using namespace simdb;
QDataStream& operator<<(QDataStream& ds, const simdb::VarVal& val)
{
    ds << val.which();
    int nestLevel = 0;
    boost::apply_visitor(simdb::DstreamWriter(nestLevel, ds), val);
    return ds;
}
QDataStream& operator>>(QDataStream& ds, simdb::VarVal& val)
{
    int valType;
    ds >> valType;

    switch (valType)
    {
    case simdb::ValueType::Void:
        val = Void();
        break;

    case simdb::ValueType::Int:
    {
        int i;
        ds >> i;
        val = i;
        break;
    }

    case simdb::ValueType::Double:
    {
        double d;
        ds >> d;
        val = d;
        break;
    }

    case simdb::ValueType::Bool:
    {
        bool b;
        ds >> b;
        val = b;
        break;
    }

    case simdb::ValueType::String:
    {
        QString s;
        ds >> s;
        val = s;
        break;
    }

    case simdb::ValueType::Vector:
    {
        ValVector vec;
        ds >> vec;
        val = vec;
        break;
    }

    case simdb::ValueType::Map:
    {
        ValMap map;
        ds >> map;
        val = map;
        break;
    }

    default:
        mgc__assert(false, "Unknown variant type on disk");
        // Skip unknown variant type
        //!\discuss : pz/cd (07/29/2015) : do we need a skipping mechanism within simdb to keep the datastream from being corrupted/stopped?
    }

    return ds;
}
