/* Copyright 2014 Mentor Graphics Corporation
    All Rights Reserved

 THIS WORK CONTAINS TRADE SECRET
 AND PROPRIETARY INFORMATION WHICH IS THE
 PROPERTY OF MENTOR GRAPHICS
 CORPORATION OR ITS LICENSORS AND IS
 SUBJECT TO LICENSE TERMS.
*/

#ifndef SIM_VALUE_H
#define SIM_VALUE_H

#include <Python.h>

#include <QString>
#include <iostream>
#include <boost/format.hpp>
#include <map>
#include <boost/enable_shared_from_this.hpp>

#include "simValueBase.h"
#include "simSerialize.h"
#include <QObject>

// To exclude code from being wrapped, use
#ifndef SWIG
#endif

namespace simdb
{

class Stream;

/*!
 * \brief A dynamically typed class accesssible from Python, holds the actual value within a SimValue
 * \details Offers similar functionality to Falcon's Mule_Value (or something like QVariant)
 */
class Value : 
    public QObject,
    public SimSerializable,
    public boost::enable_shared_from_this<Value>
{
    Q_OBJECT
    VarVal val_;
public:

    // Order is important for the constructors

    /*!
       \brief Copy constructor
     */
    Value(const Value& rhs);

    /*!
       \brief Assignment operator
     */
    Value& operator=(const Value& rhs);

    /*!
       \brief Default constructor
     */
    explicit Value();

    /*!
       \brief Pseudo copy constructor
     */
    explicit Value(ValuePtr valp);

    /*!
       \brief Constructor from int
     */
    explicit Value(int val);

    /*!
       \brief Constructor from double
     */
    explicit Value(double val);

    /*!
       \brief Constructor from bool
     */
    explicit Value(bool val);

    /*!
       \brief Constructor from QString
     */
    explicit Value(const QString & val);

    /*!
       \brief Constructor from C-string
     */
    explicit Value(const char* val);

    /*!
       \brief Constructor from QString
     */
//    explicit Value(const QString& val);

    /*!
       \brief Constructor from a vector of simdb::ValuePtr
     */
    explicit Value(const ValVector& val);

    /*!
       \brief Constructor from a vector of bool
     */
    explicit Value(const BoolVec&   bvec);

    /*!
       \brief Constructor from a vector of int
     */
    explicit Value(const IntVec&    ivec);

    /*!
       \brief Constructor from a vector of double
     */
    explicit Value(const DoubleVec& dvec);

    /*!
       \brief Constructor from a vector of QString
     */
    explicit Value(const StringVec& svec);

    /*!
       \brief Constructor from a map of QString to simdb::ValuePtr
     */
    explicit Value(const ValMap& valmap);

    /*!
       \brief Destructor
     */
    virtual ~Value();

    // Order is important for swig to function in the correct manner

    /*!
       \brief Sets the contained value

       \param valp the value whose contained value this contained value should mirror
     */
    void set(ValuePtr valp);

    /*!
       \brief Sets the contained value

       \param val the value this contained value should mirror
     */
    void set(int val);

    /*!
       \brief Sets the contained value

       \param val the value this contained value should mirror
     */
    void set(double val);

    /*!
       \brief Sets the contained value

       \param val the value this contained value should mirror
     */
    void set(bool val);

    /*!
       \brief Sets the contained value

       \param val the value this contained value should mirror
     */
    void set(const char* val);

    /*!
       \brief Sets the contained value

       \param val the value this contained value should mirror
     */
    void set(const QString& val);

    /*!
       \brief Sets the contained value

       \param bvec the value this contained value should mirror
     */
    void set(const BoolVec&    bvec);

    /*!
       \brief Sets the contained value

       \param ivec the value this contained value should mirror
     */
    void set(const IntVec&     ivec);

    /*!
       \brief Sets the contained value

       \param dvec the value this contained value should mirror
     */
    void set(const DoubleVec&  dvec);

    /*!
       \brief Sets the contained value

       \param svec the value this contained value should mirror
     */
    void set(const StringVec&  svec);

    /*!
       \brief Sets the contained value

       \param valmap the value this contained value should mirror
     */
    void set(const ValMap& valmap);


    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(ValuePtr val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(int val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(double val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(bool val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const char* val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const QString& val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const BoolVec&    val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const IntVec&     val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const DoubleVec&  val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const StringVec&  val);

    /*!
       \brief For vectors, appends another value

       \param val the value to append
     */
    void append(const ValMap& val);

    /*!
       \brief For vectors, accesses an indexed value

       \param idx the index of the value to access
     */
    ValuePtr operator[](size_t idx);

    /*!
       \brief For vectors, removes the first value that has a string representation matching \b handle

       \param handle the string to match for removal
     */
    void remove(const QString& handle);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, ValuePtr val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, int val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, double val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, bool val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const char* val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const QString& val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const BoolVec&    val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const IntVec&     val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const DoubleVec&  val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const StringVec&  val);

    /*!
       \brief For maps, inserts an element

       \param key the key of the new element
       \param val the value of the new element
     */
    void insert(const QString& key, const ValMap& val);

    /*!
       \brief For maps, finds the value of an element

       \param key the key of the element to find
     */
    ValuePtr find(const QString& key);

    /*!
       \brief Equality operator
     */
    bool operator==(const Value& rhs) const;

    /*!
       \brief Inequality operator
     */
    bool operator!=(const Value& rhs) const;

    /*!
       \brief Type query, sees if the value is void
     */
    bool isVoid()
    {
        return val_.which() == ValueType::Void;
    }

    /*!
       \brief Type query, sees if the value is an integer
     */
    bool isInt()
    {
        return val_.which() == ValueType::Int;
    }

    /*!
       \brief Type query, sees if the value is a double
     */
    bool isDouble()
    {
        return val_.which() == ValueType::Double;
    }

    /*!
       \brief Type query, sees if the value is a bool
     */
    bool isBool()
    {
        return val_.which() == ValueType::Bool;
    }

    /*!
       \brief Type query, sees if the value is a string
     */
    bool isString()
    {
        return val_.which() == ValueType::String;
    }

    /*!
       \brief Type query, sees if the value is a vector
     */
    bool isVector()
    {
        return val_.which() == ValueType::Vector;
    }

    /*!
       \brief Type query, sees if the value is a map
     */
    bool isMap()
    {
        return val_.which() == ValueType::Map;
    }

    /*!
       \brief Type query, sees if the value is a number (double or integer)
     */
    bool isNumber()
    {
        return isInt() || isDouble();
    }

    /*!
       \brief Value getter, only use if simdb::Value::isBool() returns true
     */
    bool        getBool();

    /*!
       \brief Value getter, only use if simdb::Value::isInt() returns true
     */
    int         getInt();

    /*!
       \brief Value getter, only use if simdb::Value::isDouble() returns true
     */
    double      getDouble();

    /*!
       \brief Value getter, only use if simdb::Value::isString() returns true
     */
    QString getString();

    /*!
       \brief Value getter, only use if simdb::Value::isVector() returns true
     */
    ValVector&  vector();

    /*!
       \brief Value getter, only use if simdb::Value::isMap() returns true
     */
    ValMap&     map();

    /*!
       \brief Gets the Python representation of the value (in Python-native objects)
     */
    virtual PyObject*   get();

    /*!
       \brief Gets a clone of this value
     */
    virtual ValuePtr getValue();

    /*!
       \brief Returns a string representation of the contained value (regardless of its type)
     */
    QString formStr() const;

    /*!
       \brief Returns a string representation of the type of the contained value
     */
    QString typeName() const;

    /*!
       \brief Dumps the value to the chosen stream
       \param[in] nameP an identifier to distinguish instances/for grepping
       \param[in] nestLevel how many indents to output before each entry
       \param[in,out] dumpOut the stream to output to
     */
    virtual void dump(
        const char *const nameP = NULL,    // pointer to object name
        const int nestLevel = 0,
        std::ostream& dumpOut = std::cout
    ) const ;

    /*!
       \brief For const non-mutating visitors
     */
    template <typename Visitor>
    typename Visitor::result_type apply_visitor(const Visitor& v) const
    {
        return val_.apply_visitor(v);
    }

    /*!
       \brief For const mutating visitors
     */
    template <typename Visitor>
    typename Visitor::result_type apply_visitor(const Visitor& v)
    {
        return val_.apply_visitor(v);
    }

    /*!
       \brief For non-const non-mutating visitors
     */
    template <typename Visitor>
    typename Visitor::result_type apply_visitor(Visitor& v) const
    {
        return val_.apply_visitor(v);
    }

    /*!
       \brief For non-const mutating visitors
     */
    template <typename Visitor>
    typename Visitor::result_type apply_visitor(Visitor& v)
    {
        return val_.apply_visitor(v);
    }

    /*!
       \brief Gets the simdb::ValuePtr from this as a PyObject*
       \warning Uses pointer-as-long logic
     */
//   PyObject* getSWIGProxy();

    /*!
       \brief Helper to simdb::Value::getSWIGProxy()
       \warning Uses pointer-as-long logic
     */
//   static ValuePtr getSWIGProxyS(size_t address);

    /*!
       \brief Helper to simdb::Value::getSWIGProxy()
       \warning Uses pointer-as-long logic
     */
    virtual size_t getThisAddress()
    {
        return (size_t) & (*this);
    }

    /*!
       \brief Reverse of simdb::Value::getSWIGProxy()
       \warning Uses pointer-as-long logic
     */
//   static ValuePtr fromPy(PyObject* obj);

    SER_FIELDS(
        FIELD__VAR_VALUE
    );

    DECLARE_SERIALIZABLE(Value);

    /*!
       \brief Loads a simdb::Value from a datastream

       \param[in,out] ds the datastream
       \param[in] version the serialization version (for software/format versioning)
       \param[in,out] status a status object to record errors to
     */
    static SimSerializable* createFromStream(QDataStream& ds, float version, Status& status);
protected:
    virtual void write(QDataStream& ds, Status& status);
    virtual void write(Stream& ds, Status& status);
public:
    /*!
       \brief Loads this from a datastream

       \param[in,out] ds the datastream
       \param[in,out] status a status object to record errors to
     */
    void read(QDataStream& ds, Status& status);

    friend struct EqualOp;
};

/*!
 * \brief Exception for when the type of a Value does not match
 */
class ValueTypeMismatch : public std::exception
{
    QString msg_;
public:
    ValueTypeMismatch(const QString &msg): msg_(msg) {}
    virtual ~ValueTypeMismatch() throw() {}

    virtual const char* what() const throw()
    {
        return msg_.toStdString().c_str();
    }
};

/*!
 * \brief Exception for when a index in the Value vector is out of bounds
 */
class ValueVectorIdxOutOfBounds : public std::exception
{
    QString msg_;
public:
    ValueVectorIdxOutOfBounds(const QString &msg): msg_(msg) {}
    virtual ~ValueVectorIdxOutOfBounds() throw() {}

    virtual const char* what() const throw()
    {
        return msg_.toStdString().c_str();
    }
};


extern ValuePtr value__void;
extern ValuePtr value__true;
extern ValuePtr value__false;
} // Namespace sim



#endif
