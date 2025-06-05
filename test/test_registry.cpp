#include <gtest/gtest.h>

#include "toad/registry/registry.hpp"
#include "toad/registry/registry_macro.hpp"

namespace toad::registry
{
class TestClass
{
 public:
    TestClass() = default;
    virtual ~TestClass() = default;
};
class TestClassA : public TestClass
{
 public:
    TestClassA() = default;
    ~TestClassA() override = default;
};

class TestClassB : public TestClass
{
 public:
    TestClassB() = default;
    ~TestClassB() override = default;
};

using TEST_REGISTERY = Registry<TestClass>;
REGISTER_CLASS(TEST_REGISTERY, TestClassA);
REGISTER_CLASS(TEST_REGISTERY, TestClassB);
}  // namespace toad::registry

TEST(RegistryTest, RegisterAndBuild)
{
    using namespace toad::registry;

    auto &registry = Registry<TestClass>::instance();

    // Build instances
    auto instanceA = registry.build("TestClassA");
    auto instanceB = registry.build("TestClassB");

    EXPECT_NE(instanceA, nullptr);
    EXPECT_NE(instanceB, nullptr);
}
