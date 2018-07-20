/* Copyright 2014 Mentor Graphics Corporation
    All Rights Reserved

 THIS WORK CONTAINS TRADE SECRET
 AND PROPRIETARY INFORMATION WHICH IS THE
 PROPERTY OF MENTOR GRAPHICS
 CORPORATION OR ITS LICENSORS AND IS
 SUBJECT TO LICENSE TERMS.
*/

#include "simSimValue.h"
#include "simState.h"
#include "simStatus.h"
#include "simTypeMgr.h"
#include "simGlobalStatus.h"

#include "simDbg.h"
#include "simSchema.h"
#include <sstream>
#include "simUtils.h"
#include "simSerializeOps.h"
#include "simErr.h"

using namespace dbg;

namespace simdb
{

IMPLEMENT_SERIALIZABLE(SimValue, 1.0)
SimValue::SimValue()
    : type_(0), id_(-1), flags_(INITIAL_STATE)

{}
SimValue::SimValue(StatePtr state, const QString typeName)
    : state_(state), id_(-1), flags_(INITIAL_STATE)
{
    Status status;
    type_ = state->getSchemaSet()->findType(typeName, status);
    mgc__assert(type_, "No type with name, report error");
}
SimValue::SimValue(SimValuePtr parent, SimType* type)
    : parent_(parent),
      type_(type), id_(-1), flags_(INITIAL_STATE)
{
}
SimValue::SimValue(Value val, SimValuePtr parent, SimType* type)
    :  Value(val),
       parent_(parent),
       type_(type), id_(-1), flags_(INITIAL_STATE)
{
}

void SimValue::destroy()
{
    StatePtr state = state_.lock();

    if (!state)
    {
        return;    // Assume this is field nested inside a top SimValue
    }

    state->deleteSimValue(shared_from_this());
}

void SimValue::enable()
{
    enableImp();
    emitSimValueChanged(MODIFIED);
    SimValuePtr parent = getParent().lock();

    if (parent)
        parent->getValueType()->enableChild(shared_from_this());
}

void SimValue::disable()
{
    disableImp();
    emitSimValueChanged(MODIFIED);
}

void SimValue::setEnabled(
    bool enabled)
{
    return (enabled ? enable() : disable());
}

SimValuePtr SimValue::shared_from_this()
{
    return boost::static_pointer_cast<SimValue>(Value::shared_from_this());
}

boost::shared_ptr<const SimValue> SimValue::shared_from_this() const
{
    return boost::static_pointer_cast<const SimValue>(Value::shared_from_this());
}

void SimValue::emitSimValueChanged(ModificationType reason)
{
    //This should really only be caused by blocking internal to simdb
    //To prevent errors due to partial changes, or to reduce redundant signal sending
    StatePtr state = state_.lock();

    if (signalsBlocked() || (state && state->signalsBlocked()))
        return;

    //Lower level changes get promoted so only
    //'top-level' instances have signals fired
    if (getParent().lock())
        return getParent().lock()->emitSimValueChanged(reason);

    emit simValueChanged(SimValueProxy(shared_from_this()), reason);
}

QString SimValue::getHandle() const
{
    if (getId() == -1)
        return "";

    return QString("%1$%2").arg(type_->getTypeFullName()).arg(getId());
//    QString typeName = type_->getTypeFullName();
//    QStringstream ss;
//    ss << typeName << "$" << getId();
//    return ss.str();
}

QString SimValue::getTypeName() const
{
    return type_->getTypeFullName();
}
QString SimValue::getCategory() const
{
    if (!type_->isSchema())
        return "";

    return schema_cast(type_)->getCategory();
}

bool SimValue::isTopVal() const
{
    return (id_ != -1) && (parent_.lock() == 0); // Has a +ve id, and no parent
}

StateWptr SimValue::getState() const
{
    if (state_.lock())
        return state_;

    mgc__assert(parent_.lock(), "null parent");
    SimValueWptr root = parent_;

    while (root.lock())
    {
        SimValuePtr p = root.lock();
        p = p->getParent().lock();

        if (!p)
            break;

        root = p;
    }

    StateWptr state = root.lock()->getState();
    mgc__assert(state.lock(), "null state at root");
    return state;
}
SimSchemaSetRef SimValue::getSchemaSet()
{
    StatePtr state = getState().lock();
    mgc__assert(state, "null state ptr");
    return state->getSchemaSet();
}

SimSchemaField* SimValue::getSchemaField() const
{
    if (type_->isSchemaField())
        return sfield_cast(type_);

    SimValuePtr parent = parent_.lock();

    if (!parent)
    {
        return 0;    // Top value
    }

    return parent->getSchemaField();
}

void SimValue::valueUnset()
{
    flags_ = (flags_ & ~STATE_MASK ) | UNSET;
    emitSimValueChanged(MODIFIED);
}

void SimValue::valueSet()
{
    flags_ = (flags_ & ~STATE_MASK ) | SET;
    emitSimValueChanged(MODIFIED);
}

void SimValue::valueDefault()
{
    flags_ = (flags_ & ~STATE_MASK ) | DEFAULT;
    emitSimValueChanged(MODIFIED);
}

void SimValue::markSet()
{
    valueSet();
    SimValuePtr parent = parent_.lock();

    if (!parent)
        return;

    SimSchemaField* schemaField = parent->getSchemaField();

    if (! schemaField)
        return;

    SimType* parentType = schemaField->getFieldType();

    //If simValue is part of one of a select type's specifications, call enableChild with Schema type instead of SelectType
    if (parentType->isSelectType() && parent->getType()->isSchema())
        parentType = parent->getType();

    IDBG_EXEC("sim_env",
              IDBG_MESSAGE("sim_env", "=========== SimValue::markSet, will dump parent type");
              parentType->dump();
             );
    parentType->enableChild(shared_from_this());
}
bool SimValue::hasField(ValuePtr key)
{
    Status localSt;
    getField(key, localSt);
    return localSt.ok();
}

//bool SimValue::hasField(const QString& key)
//{
//    ValuePtr k( new Value(key.toStdString()));
//    return hasField(k);
//}

bool SimValue::hasField(const QString& key)
{
    ValuePtr k( new Value(key));
    return hasField(k);
}

bool SimValue::hasField(const StringVec& key)
{
    Status localSt;
    ValuePtr k( new Value(key));
    getField(k, localSt);
    return localSt.ok();
}

void SimValue::setValue(const QString & key, const QString & value)
{
    ValuePtr k = ValuePtr(new Value(key));
    ValuePtr v = ValuePtr(new Value(value));
    Status st;
    setField(k, v, st);
}

void SimValue::setField(const QString& key, ValuePtr val, Status& status)
{
    ValuePtr v = ValuePtr(new Value(key));
    return setField(v, val, status);
}

void SimValue::setField(ValuePtr key, ValuePtr val, Status& status)
{
    getType()->setField(shared_from_this(), key, val, status);
}

void SimValue::setField(ValuePtr key, SimValuePtr value, Status& status)
{
    SimValuePtr dest = getField(key, status);

    if (status.bad())
        return;

    dest->setFrom(value, status);
}

void SimValue::appendField(ValuePtr key, ValuePtr val, Status& status)
{
    getType()->appendField(shared_from_this(), key, val, status);
}

void SimValue::appendField(ValuePtr key, SimValuePtr value, Status& status)
{
    SimValuePtr dest = getField(key, status);

    if (status.bad())
        return;

    dest->appendFrom(value, status);
}


SimValuePtr SimValue::getField(ValuePtr key, Status& status)
{
    return getType()->getField(shared_from_this(), key, 0, status);
}

SimValuePtr SimValue::getField(const QString& key, Status& status)
{
    return getField(ValuePtr(new Value(key)), status);
}

SimValue * SimValue::getValue(const QString & key)
{
    Status st;
    return getField(ValuePtr(new Value(key)), st).get();
}


SimValuePtr SimValue::getDeepField(
    const QString& fieldName,
    const std::vector<QString>& nestedSpec,
    bool followRefs)
{
    return getType()->getDeepField(shared_from_this(), fieldName, nestedSpec, followRefs);
}

SimValuePtr SimValue::getDeepField(
    const QString& fieldName)
{
    return getDeepField(fieldName, std::vector<QString>(), true);
}

bool SimValue::setDeepField(
    const QString& fieldName,
    ValuePtr value)
{
    return setDeepField(fieldName, std::vector<QString>(), true, value);
}

bool SimValue::setDeepField(
    const QString& fieldName,
    const std::vector<QString>& nestedSpec,
    bool followRefs,
    ValuePtr value)
{
    SimValuePtr simVal = getDeepField(fieldName, nestedSpec, followRefs);

    if (!simVal)
        return false;

    simdb::Status st;
    simVal->set(value, st);
    return st.ok();
}

// Python only
void SimValue::setField(ValuePtr key, ValuePtr value)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    setField(key, value, status);
}
void SimValue::setField(ValuePtr key, SimValuePtr value)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    setField(key, value, status);
}

void SimValue::setField(const StringVec& key, SimValuePtr value)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    ValuePtr k(new Value(key));
    setField(k, value, status);
}

void SimValue::appendField(ValuePtr key, ValuePtr value)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    appendField(key, value, status);
}
void SimValue::appendField(const QString& key, SimValuePtr value)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    ValuePtr k(new Value(key));
    appendField(k, value, status);
}
void SimValue::appendField(const StringVec& key, SimValuePtr value)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    ValuePtr k(new Value(key));
    appendField(k, value, status);
}

void SimValue::setFrom(SimValuePtr src, Status& status)
{
    SimType* srcType = src->getType();

    if (SimSchemaField* schemaField = src->getSchemaField())
        srcType = schemaField->getFieldType();

    SimType* destType = getType();

    if (SimSchemaField* schemaField = getSchemaField())
        destType = schemaField->getFieldType();

    if (*srcType != *destType )
    {
        status.push(SIM_ENV__VALUE_SET_FROM_FAILED_MISMATCHED_TYPES,
                    srcType->getTypeFullName(), srcType->getVersion(),
                    destType->getTypeFullName(), destType->getVersion()
                   );
        return;
    }

    SimValuePtr dest  = shared_from_this();
    destType->initValueFrom(dest, src);

    if (src->isSet())
        do
        {
            dest->markSet();
            dest = dest->getParent().lock();
        }
        while (dest);

    flags_      = src->flags_;
    emitSimValueChanged(MODIFIED);
}

void SimValue::appendFrom(SimValuePtr src, Status& status)
{
    SimType* srcType = src->getType();

    if (SimSchemaField* schemaField = src->getSchemaField())
    {
        srcType = schemaField->getFieldType();    // Make sure we reach the src type
    }

    // Has to be a vector of a compitable type (compared to src)
    SimType* destType = getType();
    mgc__assert(destType->isSchemaField(), "Expected a schema field");

    if (SimSchemaField* schemaField = getSchemaField())
    {
        if (!schemaField->isVector())
        {
            status.push(SIM_ENV__EXPECTED_A_VECTOR_OF_FIELDS);
            return;
        }

        destType = schemaField->getFieldType();
    }

    if (*srcType != *destType )
    {
        status.push(SIM_ENV__VALUE_SET_FROM_FAILED_MISMATCHED_TYPES,
                    srcType->getTypeFullName(), srcType->getVersion(),
                    destType->getTypeFullName(), destType->getVersion()
                   );
        return;
    }

    getType()->appendValueFrom(shared_from_this(), src);
    emitSimValueChanged(MODIFIED);
}

void SimValue::set(ValuePtr src, Status& status)
{
    getType()->setValueFrom(shared_from_this(), src, status);
}

void SimValue::set(ValuePtr src)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope

    if (!src)
        src = value__void;

    getType()->setValueFrom(shared_from_this(), src, status);
}

void SimValue::append(ValuePtr src, Status& status)
{
    getType()->appendValueFrom(shared_from_this(), src, status);
}
void SimValue::append(ValuePtr src)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    getType()->appendValueFrom(shared_from_this(), src, status);
}

namespace
{

template<typename ZZZ>
SimValuePtr getFieldImpl(SimValuePtr x, const ZZZ& key)
{
    ValuePtr k(new Value(key));
    return x->getField(k);
}

}//End namespace <unnamed>

SimValuePtr SimValue::getField(const char * key)
{
    return getFieldImpl(shared_from_this(), QString(key));
}

SimValuePtr SimValue::getField(const QString& key)
{
    return getFieldImpl(shared_from_this(), key);
}
SimValuePtr SimValue::getField(const std::vector<QString>& key)
{
    return getFieldImpl(shared_from_this(), key);
}
SimValuePtr SimValue::getField(int key)
{
    return getFieldImpl(shared_from_this(), key);
}
SimValuePtr SimValue::getField(ValuePtr key)
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    return getField(key, status);
}

ValuePtr SimValue::getValue()
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    ValuePtr value = value__void;

    if (isDefault())
        return getType()->getDefaultValue();

    if (isUnset())
        return value__void;

    if (isSet())
        return getType()->decodeValue(shared_from_this(), status);

    return value__void;
}

SimValuePtr SimValue::find(const QString& key)
{
    SimValuePtr hvalue = boost::dynamic_pointer_cast<SimValue, Value>(Value::find(key));
    mgc__assert(hvalue, "hier structure expected a hier ptr");
    return hvalue;
}

void SimValue::setType(SimSchemaField* sfieldP)
{
    mgc__assert(type_ == sfieldP->getFieldType(),
                "Non matching types when replacing typeP with schemaFieldP"); // Assert that they match first
    type_ = sfieldP;
}

void SimValue::setState(StatePtr state)
{
    state_ = state;
}

// SimValue serialization
SimSerializable* SimValue::createFromStream(QDataStream& ds, float version, Status& status)
{
    SimValue* value = new SimValue();
    value->read(ds, status);

    if (status.bad())
    {
        delete value;
        return 0;
    }

    return value;
}

void SimValue::write(Stream& ds, Status& status)
{
    Value::write(ds, status);
    DBDUMP( "Writing SimValue" );
    SimTypePlaceHolder* holderP = new SimTypePlaceHolder(getType());
    ds.writeField(FIELD__TYPE, holderP);
    delete holderP;
    ds.writeField(FIELD__ID,   id_);
    ds.writeField(FIELD__FLAGS,  flags_);
    ds.writeEnd();
    DBDUMP( "Done Writing SimValue" );
}

void SimValue::write(QDataStream& ds, Status& status)
{
    DBDUMP_INCR_INDENT
    Value::write(ds, status);
    DBDUMP_DECR_INDENT
    DBDUMP( "Writing SimValue" );
    SimTypePlaceHolder* holderP = new SimTypePlaceHolder(getType());
    WRITE_FIELD(ds, FIELD__TYPE,   holderP);
    delete holderP;
    WRITE_FIELD(ds, FIELD__ID,   id_);
    WRITE_FIELD(ds, FIELD__FLAGS,  flags_);
    writeEnd(ds);
    //DBDUMP( boost::str(boost::format("Wrote flags: 0x%x") % flags_) );
    DBDUMP( "Done Writing SimValue" );
}
void SimValue::read(QDataStream& ds, Status& status)
{
    Value::read(ds, status);
    DBDUMP( "Reading SimValue" );
    int tag;

    while ( ((tag = readTag(ds) ) != FIELD__END ) && (ds.status() == QDataStream::Ok ))
    {
        //DBDUMP(boost::str(boost::format("Loop: Read tag %s") % SimValue::SerFieldsStrs::inst().strs_[tag] ));
        switch (tag)
        {
        case FIELD__TYPE:
            type_ = READ_FIELD(SimTypePlaceHolder*, ds);
            IDBG_EXEC("sim_db_1",
                      IDBG_MESSAGE("sim_db_1", "SimValue associated type");
                      type_->dump();
                     );
            break;

        case FIELD__ID:
            id_ = READ_FIELD(int, ds);
            break;

        case FIELD__FLAGS:
            flags_ = READ_FIELD(Flags, ds);
            break;

        default:
            skipField(ds);
        }
    }

    DBDUMP( "Done Reading SimValue" );
}
void SimValue::postRead(SimSchemaSetRef schemaSetP, Status& status)
{
    activateType(schemaSetP, status);
    // Adjust Parent pointer
    apply_visitor(ParentSetter(shared_from_this()));
    apply_visitor(TypeActivator(schemaSetP, status));
}
void SimValue::activateType(SimSchemaSetRef schemaSetP, Status& status)
{
    // Activate the type ptr
    type_ = ((SimTypePlaceHolder*)type_)->activateType(schemaSetP, status);
}

bool SimValue::isUsable() const   // Make it const for the dumpers,
{
    SimValue* This = const_cast<SimValue*>(this);
    return getType()->isValueUsable(This->shared_from_this());
    //return getType()->isValueUsable(shared_from_this());
}

bool SimValue::equal(SimValuePtr rhs)
{
    return (id_ == rhs->id_ ? getType()->equivalent(shared_from_this(), rhs) : false);
}

QString SimValue::getStatusStr() const
{
    return QString::fromStdString(boost::str(
               //boost::format("E : %s | S : %s | U : %s | D : %s | UB : %s ")
               boost::format("Enabled: %s, Set: %s, Unset: %s, Default: %s, Useable: %s ")
               % (isEnabled() ? "T" : "F" )
               % (isSet()     ? "T" : "F" )
               % (isUnset()   ? "T" : "F" )
               % (isDefault() ? "T" : "F" )
               % (isUsable()  ? "T" : "F" )
           ));
}

void SimValue::migrate()
{
    Status& status = GlobalStatus::inst();
    GlobalStatusReporter rep; // Reports Global status when it goes out of scope
    migrate(status);
}
void SimValue::migrate(Status& status)
{
    SimType* targetType = getMigrationTargetType(status);
    mgc__assert(targetType, "null type ptr");
    migrate(targetType, status);
}
void SimValue::migrate(SimType* targetType, Status& status)
{
    // Find the target type version in the current schema set
    // We have 4 cases
    // 1) There is a newer type version in the schema set
    // 2) There is an older type in the schema set
    // 3) There is an exact match (same type name/version) in the schema set, so we need to switch type ptrs for the value
    // 4) We do not have a type with that name in the setup schema set (unknown type name for the schema set),
    //    a) we can keep the value, but we will have to merge its type to the schema set
    //    b) or we can delete the value
    mgc__assert(targetType, "null type");
    SimValuePtr destValue = targetType->createValue(SimValuePtr());
    targetType->migrateValue(shared_from_this(), destValue, status);

    if (status.ok())
    {
        // Switch the interesting pieces
        type_ = destValue->type_;
        flags_ = destValue->flags_;
        Value::set(boost::static_pointer_cast<Value>(destValue));
        // Adjust the parent pointer
        apply_visitor(ParentSetter(shared_from_this()));
    }

    emitSimValueChanged(MODIFIED);
}

SimType* SimValue::getMigrationTargetType(Status& status)
{
    Status localSt;
    SimType* valueTypeP = getValueType();
    QString typeName = valueTypeP->getTypeFullName();
    float typeVersion = valueTypeP->getVersion();
    mgc__assert( typeVersion != UNMANAGED_VERSION , "unmanaged version");
    (void) typeVersion;
    // Always try to find the latest in the schema set associated with the setup
    SimType* targetTypeP = getSchemaSet()->findType(typeName, localSt);
    status.push(localSt);
    return targetTypeP;
}
SimType* SimValue::getValueType() const
{
    if (getSchemaField())
        return getSchemaField()->getFieldType();

    return getType();
}

SimValuePtr SimValue::cloneValue()
{
    SimValuePtr cloneP = getValueType()->createValue(SimValuePtr()); // Create new sim value based on the typename
    cloneP->setState(getState().lock());
    cloneP->setId(getId());
    getValueType()->initValueFrom(cloneP, shared_from_this());
    return cloneP;
}
SimType* SimValue::getBareType() const
{
    SimType* valueTypeP = getValueType();

    if (valueTypeP->isRefType())
    {
        SimRefType* refTypeP = ref_type_cast(valueTypeP);
        valueTypeP = refTypeP->getReferencedType();
    }

    return valueTypeP;
}
bool SimValue::requiresMigration()
{
    SimType* typeP = getBareType();
    QString typeName = typeP->getTypeFullName();
    float typeVersion = typeP->getVersion();
    Status localSt;
    SimType* typeInSchemaSetP = getSchemaSet()->findType(typeName, localSt, typeVersion);
    return (typeP != typeInSchemaSetP);
}
void SimValue::checkTypePtr()
{
    assertInSchemaSet(getValueType());
}

void SimValue::assertInSchemaSet(SimType* typeP)
{
    Status localSt;
    QString typeName = typeP->getTypeFullName();
    float version = typeP->getVersion();
    SimType* typeInSchemaSetP = getSchemaSet()->findType(typeName, localSt, version);
    QString ptrStr = formatPtr(typeP);
    QString inSsetPtrStr = formatPtr(typeInSchemaSetP);
    IDBG_MESSAGE("sim_env", boost::str(boost::format("Type : %s (%g), ptr (%s)  in schema set as : %s ") %
                                       typeName %  version % ptrStr % inSsetPtrStr));
    mgc__assert(typeP == typeInSchemaSetP, "typeP is not in schema set");
}


void SimValue::adjustHandles(const HandlesMap& hmap)
{
    getType()->adjustHandles(shared_from_this(), hmap);
}

void SimValue::dump(
    const char *const nameP,    // pointer to object name
    const int         nestLevel,   // nesting level
    std::ostream& dumpOut
) const
{
    startDump("SimValue", this, nameP, nestLevel, dumpOut);
    // Value::dump("", nestLevel+1, dumpOut);
    //SimValuePtr parent = parent_.lock();
    indentDump(nestLevel + 1, dumpOut ) << "State: " << formatPtr(state_.lock().get()) << std::endl;
    indentDump(nestLevel + 1, dumpOut ) << "Parent: " << formatPtr(parent_.lock().get()) << std::endl;
    indentDump(nestLevel + 1, dumpOut ) << "Inst id: " << id_ << std::endl;
    indentDump(nestLevel + 1, dumpOut ) << "Inst handle: " << getHandle() << std::endl;

    if (type_)
    {
        QString valueStatusStr = getStatusStr();
        indentDump(nestLevel + 1, dumpOut ) << boost::format("%s, Type: %s, Ver: %.2f") % valueStatusStr %
                                            getTypeName() % getType()->getVersion() << std::endl;
        //mgc__assert(type_, "null type");
        SimValuePtr p = boost::const_pointer_cast<SimValue, const SimValue>(shared_from_this());
        type_->dumpValue(p, nestLevel + 1, dumpOut);
    }

    endDump(nestLevel, dumpOut);
}

SimValueQMetaTypeRegistrar::SimValueQMetaTypeRegistrar()
{
    qRegisterMetaType<simdb::SimValueProxy>("SimValueProxy");
    qRegisterMetaType<simdb::ModificationType>("SimValueModificationType");
    qRegisterMetaTypeStreamOperators<simdb::SimValueProxy>("SimValueProxy");
}
SimValueQMetaTypeRegistrar SimValueQMetaTypeRegistrar::inst;

void ParentSetter::operator() (const ValVector& vec) const
{
    for (size_t idx = 0; idx < vec.size(); ++idx)
    {
        SimValuePtr fieldVal = boost::dynamic_pointer_cast<SimValue, Value>(vec[idx]);
        mgc__assert(fieldVal, "null field val");
        fieldVal->setParent(parent_);
        boost::apply_visitor(ParentSetter(fieldVal), *(vec[idx]));
    }
}

void ParentSetter::operator() (const ValMap& val) const
{
    ValMap::const_iterator vit;

    for (vit = val.begin(); vit != val.end(); ++vit)
    {
        SimValuePtr fieldVal = boost::dynamic_pointer_cast<SimValue, Value>(vit->second);
        mgc__assert(fieldVal, "null field val");
        fieldVal->setParent(parent_);
        boost::apply_visitor(ParentSetter(fieldVal), *(vit->second));
    }
}

void TypeActivator::operator() (const ValVector& vec) const
{
    for (size_t idx = 0; idx < vec.size(); ++idx)
    {
        SimValuePtr fieldVal = boost::dynamic_pointer_cast<SimValue, Value>(vec[idx]);
        mgc__assert(fieldVal, "null field val");
        fieldVal->activateType(schemaSet_, status_);
        boost::apply_visitor(TypeActivator(schemaSet_, status_), *(vec[idx]));
    }
}

void TypeActivator::operator() (const ValMap& val) const
{
    ValMap::const_iterator vit;

    for (vit = val.begin(); vit != val.end(); ++vit)
    {
        SimValuePtr fieldVal = boost::dynamic_pointer_cast<SimValue, Value>(vit->second);
        mgc__assert(fieldVal, "null field val");
        fieldVal->activateType(schemaSet_, status_);
        boost::apply_visitor(TypeActivator(schemaSet_, status_), *(vit->second));
    }
}

