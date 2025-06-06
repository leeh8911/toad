#pragma once

namespace toad::mixin
{
template <typename T>
class Singleton
{
 public:
    static T& instance()
    {
        static T instance;
        return instance;
    }

    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    Singleton(Singleton&&) = delete;
    Singleton& operator=(Singleton&&) = delete;

 protected:
    Singleton() = default;
    ~Singleton() = default;

    // Allow derived classes to access the constructor and destructor
    friend T;
};
}  // namespace toad::mixin
