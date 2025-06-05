#pragma once

#include <functional>
#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace toad::registry
{
template <typename T>
class Registry
{
 public:
    using value_type = T;
    using CreatorFunc = std::function<std::unique_ptr<T>()>;

    // 싱글턴 인스턴스 얻기
    static Registry<T> &instance()
    {
        static Registry<T> inst;
        return inst;
    }

    // 클래스 이름(name)과 생성자 함수(creator)를 등록
    // 동일한 이름이 이미 등록되어 있으면 false 반환
    bool register_class(const std::string &name, CreatorFunc creator)
    {
        auto it = creators.find(name);
        if (it == creators.end())
        {
            creators.emplace(name, std::move(creator));
            return true;
        }
        return false;
    }

    // 등록된 이름(name)에 따라 객체 생성
    std::unique_ptr<T> build(const std::string &name) const
    {
        auto it = creators.find(name);
        if (it == creators.end())
        {
            throw std::runtime_error("Registry: \"" + name + "\" not registered.");
        }
        return (it->second)();
    }

    // (디버깅용) 현재 등록된 모든 이름을 벡터로 반환
    std::vector<std::string> registered_names() const
    {
        std::vector<std::string> names;
        names.reserve(creators.size());
        for (auto &p : creators)
        {
            names.push_back(p.first);
        }
        return names;
    }

 private:
    Registry() = default;
    ~Registry() = default;
    Registry(const Registry &) = delete;
    Registry &operator=(const Registry &) = delete;

    std::unordered_map<std::string, CreatorFunc> creators;
};
}  // namespace toad::registry
