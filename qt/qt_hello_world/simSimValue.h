/* Copyright 2014 Mentor Graphics Corporation
    All Rights Reserved

 THIS WORK CONTAINS TRADE SECRET
 AND PROPRIETARY INFORMATION WHICH IS THE
 PROPERTY OF MENTOR GRAPHICS
 CORPORATION OR ITS LICENSORS AND IS
 SUBJECT TO LICENSE TERMS.
*/

#ifndef SIM_HIER_VALUE_H
#define SIM_HIER_VALUE_H

#include "simBase.h"
#include "simValueBase.h"
#include "simStateBase.h"
#include "simValue.h"

#include <QtCore/QMetaType>
#include <QtCore/QObject>
#include <QDebug>

namespace simdb
{

class    Stream;
class    SimType;
class    SimSchemaField;
class    Status;
struct   ParentSetter;
struct   TypeActivator;
class IdMgr;


/*!
 * \brief The class for associating a schema type with a value hierarchically
 * \details This is the main class for simulation settings
 */
class SimValue :
    public Value
{

    Q_OBJECT

public slots:

    /*!
       \brief Queries if the simdb::SimValue has a given [potentially nested/hierarchical] field

       \param[in] key the field specification
     */
    bool hasField(ValuePtr key);

    bool hasField(const QString & key);

    /*!
       \brief Queries if the simdb::SimValue has a given field

       \param[in] key the fieldname
     */
//    bool hasField(const QString& key);

    /*!
       \brief Queries if the simdb::SimValue has a given nested field

       \param[in] key the field specification
     */
    bool hasField(const StringVec& key);

    /*!
       \brief Set a given field with a given value

       \param[in] key the field specification
       \param[in] value the value

       \note reports status
     */
    void setField(ValuePtr key, ValuePtr value);

    /*!
       \brief Set a given field with a given value

       \param[in] key the field specification
       \param[in] value the value

       \note reports status
     */
    void setField(ValuePtr key, SimValuePtr value);

    void setValue(const QString & key, const QString & value);

    QString toStr();
    //QString toStr(const QString & bar);

    /*!
       \brief Appends a given value to a given field (used with vector fields)

       \param[in] key the field specification
       \param[in] value the value to append

       \note reports status
     */
    void appendField(ValuePtr key, ValuePtr value);

    /*!
       \brief Appends a given value to a given field (used with vector fields)

       \param[in] key the fieldname
       \param[in] value the value to append

       \note reports status
     */
    void appendField(const QString& key, SimValuePtr value);

    /*!
       \brief Sets the underlying value to a given value

       \param[in] src what the underlying value should be set to

       \note reports status
     */
    void set(ValuePtr src);

    /*!
       \brief Appends a given value the underlying value (used when this is a vector)

       \param[in] src what the underlying value should have appended to it

       \note reports status
     */
    void append(ValuePtr src);

    /*!
       \brief Get the field of a given name

       \param[in] key the name of the field to get

       \note reports status
     */
    SimValuePtr getField(const char * key);

    /*!
       \brief Get the field of a given name

       \param[in] key the name of the field to get

       \note reports status
     */
    SimValuePtr getField(const QString& key);

    simdb::SimValue * getValue(const QString & key);

    /*!
       \brief Get a nested field

       \param[in] key the specification of the field to get

       \note reports status
     */
    SimValuePtr getField(const std::vector<QString>& key);

    /*!
       \brief Get the field of a given index (used with vector fields)

       \param[in] key the index of the field to get

       \note reports status
     */
    SimValuePtr getField(int key);

    /*!
       \brief Get a [potentially nested] field

       \param[in] key the specification of the field to get

       \note reports status
     */
    SimValuePtr getField(ValuePtr key);

    /*!
       \brief Gets a field of a given name
       \details Returns the <b>first</b> field found
       \details This does a <b>depth-first</b> search (dives into SimSelectTypes, SimSchemas and SimRefTypes)

       \warning Null ptr returned on any error

       \param[in] fieldName the name of the field to find
     */
    SimValuePtr getDeepField(
        const QString& fieldName);

    /*!
       \brief Gets a field of a given name
       \details Returns the <b>first</b> field found
       \details This does a <b>depth-first</b> search (dives into SimSelectTypes, SimSchemas and potentially SimRefTypes)

       \warning Null ptr returned on any error

       \param[in] fieldName the name of the field to find
       \param[in] nestedSpec an ordered collection of strings that must be matched along the dive in order to return a positive result (used for disambiguation purposes)
       \param[in] followRefs whether to follow references or not
     */
    SimValuePtr getDeepField(
        const QString& fieldName,
        const std::vector<QString>& nestedSpec,
        bool followRefs);

    //! \cond
    SimValuePtr shared_from_this();
    boost::shared_ptr<const SimValue>  shared_from_this() const;
    //! \endcond

//SWIG has trouble wrapping these (it puts the templates in an odd order)
//but approximations of these are available in python due to .i file %extend code
    /*!
       \brief Sets a field of a given name to the given value
       \details Uses the same logic as simdb::SimValue::getDeepField()

       \param[in] fieldName the name of the field to find
       \param[in] value the value to set the field to

       \result if the field was found and could be set to the value with no problems
     */

public:
    bool setDeepField(
        const QString& fieldName,
        ValuePtr value);

    //! \cond
    template<typename V>
    bool setDeepField(
        const QString& fieldName,
        const V& value);
    //! \endcond

    /*!
       \brief Sets a field of a given name to the given value
       \details Uses the same logic as simdb::SimValue::getDeepField()

       \param[in] fieldName the name of the field to find
       \param[in] nestedSpec an ordered collection of strings that must be matched along the dive in order to return a positive result (used for disambiguation purposes)
       \param[in] followRefs whether to follow references or not
       \param[in] value the value to set the field to

       \result if the field was found and could be set to the value with no problems
     */
    bool setDeepField(
        const QString& fieldName,
        const std::vector<QString>& nestedSpec,
        bool followRefs,
        ValuePtr value);
    //! \cond
    template<typename V>
    bool setDeepField(
        const QString& fieldName,
        const std::vector<QString>& nestedSpec,
        bool followRefs,
        const V& value);
    //! \endcond

    /*!
       \brief Set a given field with a given value

       \param[in] key the field specification
       \param[in] value the value

       \note reports status
     */
    void setField(const StringVec& key, SimValuePtr value);

    //! \cond
    template<typename K, typename V>
    void setField(K key, V value);
    //! \endcond

    /*!
       \brief Appends a given value to a given field (used with vector fields)

       \param[in] key the field specification
       \param[in] value the value to append

       \note reports status
     */
    void appendField(const StringVec& key, SimValuePtr value);

    //! \cond
    template<typename K, typename V>
    void appendField(K key, V value);

    template<typename V>
    void set(V value);

    template<typename V>
    void append(V value);
    //! \endcond

    /*!
       \brief Enables the simdb::SimValue
     */
    void enable();

    /*!
       \brief Disables the simdb::SimValue
     */
    void disable();

    /*!
       \brief Sets the enabled status of the simdb::SimValue
       \param[in] enabled whether to enable or disable the simdb::SimValue
     */
    void setEnabled(bool enabled);

    /*!
       \brief Unsets the simdb::SimValue
     */
    void unset()
    {
        return valueUnset();
    }

    /*!
       \brief Returns if the simdb::SimValue is enabled
     */
    bool isEnabled()  const
    {
        return flags_ & ENABLED;
    }

    /*!
       \brief Returns if the simdb::SimValue is unset (as opposed to set/default)
     */
    bool isUnset()    const
    {
        return (flags_ & STATE_MASK) == UNSET;
    }

    /*!
       \brief Returns if the simdb::SimValue is set (as opposed to unset/default)
     */
    bool isSet()      const
    {
        return (flags_ & STATE_MASK) == SET;
    }

    /*!
       \brief Returns if the simdb::SimValue is default (as opposed to set/unset)
     */
    bool isDefault()  const
    {
        return (flags_ & STATE_MASK) == DEFAULT;
    }

    /*!
       \brief Use at own risk
       \deprecated
     */
    bool isUsable()  const;

    /*!
       \brief Returns if this value contains similar values and hierarchy as the passed value (for internal/testing use only)
       \details Used with sandboxing to determine if two values from different states (of the same simulator) are equivalent
     */
    bool equal(SimValuePtr rhs);

    /*!
       \brief Get the type, can be a field or a real type
     */
    SimType* getType() const
    {
        return type_;
    }

    /*!
       \brief Get the handle of this value
     */
    QString getHandle() const;

    /*!
       \brief Destroy this value, unregister it with the state
       \details This is used for performance reasons (don't have to re-find the value to destroy)
     */
    void destroy();

    /*!
       \brief Get the field in the case that the value is associated with a schema field
     */
    SimSchemaField* getSchemaField() const;

    /*!
       \brief Get the perceived value
       \details Uses the set/unset/default flags to get the perceived value of the underlying value
     */
    virtual ValuePtr getValue();

    /*!
       \brief Helper to simdb::SimValue::getSWIGProxy()
       \warning Uses pointer-as-long logic
     */
    static SimValuePtr getSWIGProxyS(size_t address);
    /*!
       \brief Helper to simdb::SimValue::getSWIGProxy()
       \warning Uses pointer-as-long logic
     */
    virtual size_t getThisAddress()
    {
        return (size_t) & (*this);
    }

    //! \cond
    //Testing Only
    void formatterTest();
    void migrate();
    //! \endcond

#ifndef SWIG
private:
    typedef unsigned short Flags;
    enum
    {
        NULLVAL        = 0x00,
        UNSET          = 0x01,
        SET            = 0x02,
        DEFAULT        = 0x03,
        //   more ?
        //               0x06,
        //   up to       0x07,
        STATE_MASK     = 0x07,

        // More flags
        ENABLED        = 0x08,
        // More flags  = 0x10
        // More flags  = 0x20
        INITIAL_STATE  = UNSET | ENABLED
    };


    StateWptr         state_;
    SimValueWptr      parent_;
    SimType*          type_;
    int               id_;
    Flags             flags_;    // Flags associated with the value

public slots:
    SimValue * new_SimValue()
    {
        return new SimValue();
    }
public:


    /*!
       \brief Default constructor (for internal simdb use only)
     */
    SimValue();

    /*!
       \brief State-based constructor (for internal simdb use only)

       \param[in] state the simdb::State to construct the simdb::SimValue in
       \param[in] typeName the name of the type the constructed value should reference
     */
    SimValue(StatePtr state, const QString typeName);

    /*!
       \brief Parent-based constructor (for internal simdb use only)

       \param[in] parent the parent of the created simdb::SimValue
       \param[in] type the type the constructed value should reference
     */
    SimValue(SimValuePtr parent, SimType* type);

    /*!
       \brief Parent-based constructor (for internal simdb use only)

       \param[in] val the underlying value the created simdb::SimValue should have
       \param[in] parent the parent of the created simdb::SimValue
       \param[in] type the type the constructed value should reference
     */
    SimValue(Value val, SimValuePtr parent, SimType* type);

    /*!
       \brief Retrieves the unique id of the simdb::SimValue for this' particular type
     */
    int         getId() const
    {
        return id_;
    }

    /*!
       \brief Retrieves this' particular type's name
     */
    QString getTypeName() const;

    /*!
       \brief Retrieves this' particular type's category
     */
    QString getCategory() const;

    /*!
       \brief Returns if this has a parent value
     */
    bool isTopVal() const;

    /*!
       \brief Returns the parent value
       \result a weak pointer to the parent value
     */
    SimValueWptr getParent()
    {
        return parent_;
    }

    /*!
       \brief Returns the containing simdb::State
       \result a weak pointer to the containing simdb::State
     */
    StateWptr    getState() const;

    /*!
       \brief Returns the containing schema set, if it exists
       \warning if no containing state exists, this will Crash/assert
       \result a shared pointer to the containing simdb::SchemaSet
       \todo : cd (12-01-2015) : fix so this won't crash, potentially remove?
     */
    SimSchemaSetRef getSchemaSet();

    /*!
       \brief Sets the underlying value to a given value

       \param[in] src what the underlying value should be set to
       \param[in,out] status a status object to record errors to
     */
    void set(ValuePtr src, Status& status);

    /*!
       \brief Appends a given value the underlying value (used when this is a vector)

       \param[in] src what the underlying value should have appended to it
       \param[in,out] status a status object to record errors to
     */
    void append(ValuePtr src, Status& status);

    /*!
       \brief Set a given field with a given value

       \param[in] key the field specification
       \param[in] value the value
       \param[in,out] status a status object to record errors to
     */
    void setField(const QString& key, ValuePtr value, Status& status);

    /*!
       \brief Set a given field with a given value

       \param[in] key the field specification
       \param[in] value the value
       \param[in,out] status a status object to record errors to
     */
    void setField(ValuePtr key, ValuePtr value, Status& status);

    /*!
       \brief Set a given field with a given value

       \param[in] key the field specification
       \param[in] value the value
       \param[in,out] status a status object to record errors to
     */
    void setField(ValuePtr key, SimValuePtr value, Status& status);

    /*!
       \brief Appends a given value to a given field (used with vector fields)

       \param[in] key the field specification
       \param[in] value the value to append
       \param[in,out] status a status object to record errors to
     */
    void appendField(ValuePtr key, ValuePtr value, Status& status);

    /*!
       \brief Appends a given value to a given field (used with vector fields)

       \param[in] key the field specification
       \param[in] value the value to append
       \param[in,out] status a status object to record errors to
     */
    void appendField(ValuePtr key, SimValuePtr value, Status& status);

    /*!
       \brief Get a field

       \param[in] key the specification of the field to get
       \param[in,out] status a status object to record errors to
     */
    SimValuePtr getField(ValuePtr key, Status& status);

    /*!
       \brief Get a field

       \param[in] key the specification of the field to get
       \param[in,out] status a status object to record errors to
     */
    SimValuePtr getField(const QString& key, Status& status);

    /*!
       \brief Set starting from another SimValue, check types

       \param[in] src the value to copy
       \param[in,out] status a status object to record errors to
     */
    void setFrom(SimValuePtr src, Status& status);

    /*!
       \brief Append starting from another SimValue, check types (used with vector fields)

       \param[in] src the value to copy
       \param[in,out] status a status object to record errors to
     */
    void appendFrom(SimValuePtr src, Status& status);

    /*!
       \brief Sets the enable flags to enabled (for internal simdb use only)
     */
    void enableImp()
    {
        flags_ |= ENABLED;
    }

    /*!
       \brief Sets the enable flags to disabled (for internal simdb use only)
     */
    void disableImp()
    {
        flags_ &= ~ENABLED;
    }

    /*!
       \brief Finds the entry with the key \b key

       \param[in] key the key to search for
     */
    SimValuePtr find(const QString& key);

    /*!
       \brief Override the type by a schema field, will not allow passing the base type

       \param[in] sfieldP a schemafield whose fieldType() will be this' new type
     */
    void setType(SimSchemaField* sfieldP);

    /*!
       \brief Override the containing state

       \param[in] state the new containing state
     */
    void setState(StatePtr state);

    // Binary write/read
    SER_FIELDS(
        FIELD__TYPE,
        FIELD__ID,
        FIELD__FLAGS
    );

    DECLARE_SERIALIZABLE(SimValue);

    /*!
       \brief Loads a simdb::SimValue from a datastream

       \param[in,out] ds the datastream
       \param[in] version the serialization version (for software/format versioning)
       \param[in,out] status a status object to record errors to
     */
    static SimSerializable* createFromStream(QDataStream& ds, float version, Status& status);

    /*!
       \brief Writes a simdb::SimValue to a stream

       \param[in,out] ds the stream to write to
       \param[in,out] status a status object to record errors to
     */
    virtual void write(Stream& ds, Status& status);

protected:
    virtual void write(QDataStream& ds, Status& status);

public:
    /*!
       \brief Loads this from a datastream

       \param[in,out] ds the datastream
       \param[in,out] status a status object to record errors to
     */
    void read(QDataStream& ds, Status& status);

    /*!
       \brief Post read cleanup/management

       \param[in] schemaSetP the schemaSet this [will] belong to/
       \param[in,out] status a status object to record errors to
     */
    virtual void postRead(SimSchemaSetRef schemaSetP, Status& status);
private:
    virtual void activateType(SimSchemaSetRef schemaSetP, Status& status);

public slots:
    // End Binary write/read

    // The following three are mutually exclusive
    /*!
       \brief Marks this as unset (as opposed to set/default)
     */
    void valueUnset();

    /*!
       \brief Marks this as set (as opposed to unset/default)
     */
    void valueSet();

    /*!
       \brief Marks this as default (as opposed to unset/set)
     */
    void valueDefault();

    /*!
       \brief Marks this as set (also traverses hierarchically upwards and marks them as enabled/set)
     */
    void markSet();

    /*!
       \brief Gets the type of this value
       \details Dereferences refTypes for their underlying type, also follows schemaFields to get their underlying type
     */
    SimType* getBareType() const;

    /*!
       \brief Finds if this needs to be migrated
     */
    bool requiresMigration();

    /*!
       \brief Dumps the value (and its subvalues and flags) to the chosen stream
       \param[in] nameP an identifier to distinguish instances/for grepping
       \param[in] nestLevel how many indents to output before each entry
       \param[in,out] dumpOut the stream to output to
     */
    void dump(
        const char *const nameP = NULL,    // pointer to object name
        const int nestLevel = 0,
        std::ostream& dumpOut = std::cout
    ) const ;

    /*!
       \brief Used by dump, gets the values of the various flags associated with this value
     */
    QString getStatusStr() const ;

    /*!
       \brief Migrate to the latest version known for the schemaSet_ associated with the setup

       \param[in,out] status a status object to record errors to
     */
    void migrate(Status& status);

    /*!
       \brief Migrate to the specified version

       \param[in] targetType the type (of a particular version) to migrate to
       \param[in,out] status a status object to record errors to
     */
    void migrate(SimType* targetType, Status& status);

    /*!
       \brief Get the latest version known for the schemaSet_ associated with the setup

       \param[in,out] status a status object to record errors to
     */
    SimType* getMigrationTargetType(Status& status);

    /*!
       \brief Get the type of associated with this, for schemafields, get the underlying fieldType()
     */
    SimType* getValueType() const;

    /*!
       \brief Create an exact clone of this value (for internal simdb use only)
     */
    SimValuePtr cloneValue();

    /*!
       \brief Check if the type ptr is assigned correctly recursively (via assertions)
     */
    void checkTypePtr();

    /*!
       \brief Check if the type ptr is assigned correctly recursively (via assertions)
     */
    void assertInSchemaSet(SimType* typeP);

    /*!
       \brief Reassigns values to RefType-typed fields to re-establish referenced links when renaming/other oddities occur
     */
    void adjustHandles(const HandlesMap& hmap);


    /*!
       \brief Emits signals to notify listeners that this has changed (for internal simdb use only)

       \param reason a clue as to how the value has changed
     */
    void emitSimValueChanged(simdb::ModificationType reason);

signals:
    /*!
       \brief It is generally not a good idea to connect to this signal due to the constant deletion/creation of values
       \brief Use the simenv::ModificationTracker instead.
     */
    void simValueChanged(
        simdb::SimValueProxy inst,
        simdb::ModificationType reason);
private:
    void setId(int id)
    {
        emitSimValueChanged(PRERENAME);
        id_ = id;
        emitSimValueChanged(RENAMED);
    }
    void setParent(SimValuePtr parent)
    {
        parent_ = parent;
    }
    //void set(SimValuePtr val);
    friend class simdb::State;
    friend class simdb::SimType;
    friend struct simdb::ParentSetter;
    friend struct simdb::TypeActivator;
    friend class simdb::IdMgr;
#endif
};

/*!
 * \brief Adjusts Parent pointer for SimValue after disk restore
 */
struct ParentSetter : public boost::static_visitor<>
{
    SimValuePtr       parent_;
    ParentSetter(SimValuePtr parent)
        : parent_(parent)
    {}

    // template <typename T>
    //    void operator() (T& operand) const {
    //       os_ << operand << std::endl;
    //    }
    //No-op for primitive types
    void operator() (Void val) const
    {
        Q_UNUSED(val);
    }
    void operator() (const int val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const double val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const bool val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const QString& val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const ValuePtr& valp) const
    {
        Q_UNUSED(valp)
    }

    void operator() (const ValVector& vec) const;
    void operator() (const ValMap& val) const;
};
/*!
 * \brief Activates a type ptr
 */
struct TypeActivator : public boost::static_visitor<>
{
    SimSchemaSetRef   schemaSet_;
    Status&           status_;
    TypeActivator(SimSchemaSetRef schemaSetP, Status& status )
        : schemaSet_(schemaSetP),
          status_(status)
    {}

    // template <typename T>
    //    void operator() (T& operand) const {
    //       os_ << operand << std::endl;
    //    }
    //No-op for primitive types
    void operator() (Void val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const int val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const double val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const bool val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const QString& val) const
    {
        Q_UNUSED(val)
    }
    void operator() (const ValuePtr& valp) const
    {
        Q_UNUSED(valp)
    }

    void operator() (const ValVector& vec) const;
    void operator() (const ValMap& val) const;
};

#ifndef SWIG
/*!
 * \brief Registers simDB related QMetaTypes for use later
 */
class SimValueQMetaTypeRegistrar
{
private:
    SimValueQMetaTypeRegistrar();
    static SimValueQMetaTypeRegistrar inst;
};

template<typename V>
bool SimValue::setDeepField(
    const QString& fieldName,
    const V& value)
{
    ValuePtr v(new Value(value));
    return setDeepField(fieldName, v);
}

template<typename V>
bool SimValue::setDeepField(
    const QString& fieldName,
    const std::vector<QString>& nestedSpec,
    bool followRefs,
    const V& value)
{
    ValuePtr v(new Value(value));
    return setDeepField(fieldName, nestedSpec, followRefs, v);
}

template<typename K, typename V>
void SimValue::setField(K key, V value)
{
    ValuePtr k(new Value(key));
    ValuePtr v(new Value(value));
    setField(k, v);
}

template<typename K, typename V>
void SimValue::appendField(K key, V value)
{
    ValuePtr k(new Value(key));
    ValuePtr v(new Value(value));
    appendField(k, v);
}

template<typename V>
void SimValue::set(V value)
{
    ValuePtr v(new Value(value));
    set(v);
}

template<typename V>
void SimValue::append(V value)
{
    ValuePtr v(new Value(value));
    append(v);
}

#endif

}

#ifndef SWIG
Q_DECLARE_METATYPE(simdb::SimValueProxy)
Q_DECLARE_METATYPE(simdb::ModificationType)

QDataStream& operator<<(QDataStream& out, const simdb::SimValueProxy& myObj);
QDataStream& operator>>(QDataStream& in, simdb::SimValueProxy& myObj);

#include <QtCore/QHash>
template<typename ZZZ>
uint qHash(const boost::shared_ptr<ZZZ>& ptr)
{
    return qHash(reinterpret_cast<quintptr>(ptr.get()));
}

#endif

#endif
