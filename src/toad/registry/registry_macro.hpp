#pragma once

#include "registry.hpp"
#include <type_traits>

// ------------------------------------------------------------------------
// 1) 매크로 오버로드를 위한 헬퍼: 인자 개수를 세어서, 적절한 REGISTER_CLASS# 매크로를 선택
// ------------------------------------------------------------------------
// __VA_ARGS__의 인자 개수가 3개면 REGISTER_CLASS3가, 2개면 REGISTER_CLASS2가
#define GET_REGISTER_CLASS_MACRO(_1, _2, _3, NAME, ...) NAME

// ------------------------------------------------------------------------
// 2) 두 개 인자로 호출할 때: ConcreteClass 이름을 자동으로 문자열화
//    (RegistryAlias, ConcreteClass)
// ------------------------------------------------------------------------
#define REGISTER_CLASS2(RegistryAlias, ConcreteClass)                                           \
    namespace                                                                                   \
    {                                                                                           \
    struct ConcreteClass##Registrar                                                             \
    {                                                                                           \
        ConcreteClass##Registrar()                                                              \
        {                                                                                       \
            static_assert(std::is_base_of_v<typename RegistryAlias::value_type, ConcreteClass>, \
                          #ConcreteClass " must derive from registry base");                    \
            RegistryAlias::instance().register_class(                                           \
                /* 문자열화 */ #ConcreteClass,                                                  \
                []() -> std::unique_ptr<typename RegistryAlias::value_type>                     \
                { return std::make_unique<ConcreteClass>(); });                                 \
        }                                                                                       \
    };                                                                                          \
    static ConcreteClass##Registrar global_##ConcreteClass##Registrar;                          \
    }

// ------------------------------------------------------------------------
// 3) 세 개 인자로 호출할 때: 세 번째 인자인 str_name을 그대로 사용
//    (RegistryAlias, ConcreteClass, str_name)
// ------------------------------------------------------------------------
#define REGISTER_CLASS3(RegistryAlias, ConcreteClass, str_name)                                 \
    namespace                                                                                   \
    {                                                                                           \
    struct ConcreteClass##Registrar                                                             \
    {                                                                                           \
        ConcreteClass##Registrar()                                                              \
        {                                                                                       \
            static_assert(std::is_base_of_v<typename RegistryAlias::value_type, ConcreteClass>, \
                          #ConcreteClass " must derive from registry base");                    \
            RegistryAlias::instance().register_class(                                           \
                /* 세 번째 인자를 키로 사용 */ str_name,                                        \
                []() -> std::unique_ptr<typename RegistryAlias::value_type>                     \
                { return std::make_unique<ConcreteClass>(); });                                 \
        }                                                                                       \
    };                                                                                          \
    static ConcreteClass##Registrar global_##ConcreteClass##Registrar;                          \
    }

// ------------------------------------------------------------------------
// 4) 실제로 사용자가 호출하는 매크로: 인자 개수에 따라 REGISTER_CLASS2 또는 REGISTER_CLASS3 선택
// ------------------------------------------------------------------------
#define REGISTER_CLASS(...) \
    GET_REGISTER_CLASS_MACRO(__VA_ARGS__, REGISTER_CLASS3, REGISTER_CLASS2)(__VA_ARGS__)
