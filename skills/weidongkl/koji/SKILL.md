# Koji Skill - Koji 构建系统

## 技能描述 | Skill Description

**名称 | Name:** koji  
**版本 | Version:** 1.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** Koji Build System (Fedora/CentOS/RHEL)  

全面的 Koji 构建系统管理技能，支持构建任务、包管理、标签、仓库、用户管理等所有核心功能。

Comprehensive Koji Build System management skill with full API coverage for build tasks, package management, tags, repositories, user management, and all core functionalities.

---

## 功能列表 | Features

### 1. 构建管理 | Build Management
- 创建构建任务 | Create build tasks
- 查看构建状态 | View build status
- 取消构建 | Cancel builds
- 重试失败构建 | Retry failed builds
- 获取构建日志 | Get build logs
- 列出构建历史 | List build history

### 2. 包管理 | Package Management
- 列出/搜索包 | List/Search packages
- 获取包信息 | Get package info
- 包所有权管理 | Package ownership
- 添加/删除包 | Add/Remove packages

### 3. 标签管理 | Tag Management
- 创建/删除标签 | Create/Delete tags
- 标签继承配置 | Tag inheritance
- 标签包列表 | Tag package list
- 标签外部仓库 | Tag external repos

### 4. 任务管理 | Task Management
- 任务状态查询 | Task status query
- 任务结果获取 | Task results
- 任务取消 | Task cancellation
- 任务日志 | Task logs

### 5. 用户管理 | User Management
- 用户信息查询 | User info query
- 用户权限管理 | User permissions
- 用户构建列表 | User builds list

### 6. SRPM/RPM 管理 | SRPM/RPM Management
- SRPM 上传 | SRPM upload
- RPM 下载 | RPM download
- 构建产物查询 | Build artifacts query

---

## 配置 | Configuration

### Koji 配置文件 | Koji Config File

位置 | Location: `~/.koji/config`

```ini
[koji]
server = https://koji.fedoraproject.org/kojihub
weburl = https://koji.fedoraproject.org/koji
topdir = ~/koji

# 认证方式 | Authentication
auth_method = kerberos
# 或 | or
# auth_method = ssl
# ssl_cert = ~/.koji/client.crt
# ssl_key = ~/.koji/client.key
```

### 环境变量 | Environment Variables

```bash
export KOJI_CONF=~/.koji/config
export KOJI_DIR=~/koji
```

---

## 使用示例 | Usage Examples

### 构建操作 | Build Operations

```bash
# 从 SRPM 构建
# Build from SRPM
koji build --target "f39" "./package-1.0-1.fc39.src.rpm"

# 从 Git 构建 (DistGit)
# Build from Git (DistGit)
koji build --target "f39" --git "https://src.fedoraproject.org/rpms/package.git"

# 查看构建信息
# View build info
koji build-info 123456

# 查看构建日志
# View build logs
koji build-logs 123456

# 取消构建
# Cancel build
koji cancel-build 123456

# 重试构建
# Retry build
koji retry-build 123456
```

### 包管理 | Package Management

```bash
# 搜索包
# Search packages
koji list-packages --query "mypackage"

# 获取包信息
# Get package info
koji package-info "mypackage"

# 列出包维护者
# List package owners
koji list-owners "mypackage"

# 添加包维护者
# Add package owner
koji add-owner "mypackage" "username"

# 删除包维护者
# Remove package owner
koji remove-owner "mypackage" "username"
```

### 标签管理 | Tag Management

```bash
# 列出所有标签
# List all tags
koji list-tags

# 获取标签信息
# Get tag info
koji tag-info "f39-updates"

# 创建标签
# Create tag
koji create-tag --name "f39-custom" --parent "f39"

# 删除标签
# Delete tag
koji delete-tag "f39-custom"

# 列出标签下的包
# List packages in tag
koji list-tag-packages "f39-updates"

# 添加包到标签
# Add package to tag
koji add-to-tag "f39-updates" "mypackage-1.0-1"

# 从标签删除包
# Remove package from tag
koji remove-from-tag "f39-updates" "mypackage-1.0-1"
```

### 任务管理 | Task Management

```bash
# 查看任务状态
# View task status
koji task-info 789012

# 查看任务结果
# View task results
koji task-results 789012

# 取消任务
# Cancel task
koji cancel-task 789012

# 查看任务日志
# View task logs
koji task-logs 789012
```

### 用户管理 | User Management

```bash
# 查看用户信息
# View user info
koji user-info "username"

# 查看用户权限
# View user permissions
koji user-permissions "username"

# 列出用户构建
# List user builds
koji list-builds --user "username"
```

### SRPM/RPM 管理 | SRPM/RPM Management

```bash
# 上传 SRPM
# Upload SRPM
koji upload-srpm "./package-1.0-1.fc39.src.rpm"

# 下载构建产物
# Download build artifacts
koji download-build 123456 --arch "x86_64"

# 下载 RPM
# Download RPM
koji download-rpm "package-1.0-1.fc39.x86_64.rpm"
```

---

## 命令参考 | Command Reference

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `build` | 创建构建 | Create build |
| `build-info` | 构建信息 | Build info |
| `build-logs` | 构建日志 | Build logs |
| `cancel-build` | 取消构建 | Cancel build |
| `retry-build` | 重试构建 | Retry build |
| `package-info` | 包信息 | Package info |
| `list-owners` | 列出维护者 | List owners |
| `add-owner` | 添加维护者 | Add owner |
| `remove-owner` | 删除维护者 | Remove owner |
| `tag-info` | 标签信息 | Tag info |
| `create-tag` | 创建标签 | Create tag |
| `delete-tag` | 删除标签 | Delete tag |
| `list-tag-packages` | 标签包列表 | Tag packages |
| `add-to-tag` | 添加到标签 | Add to tag |
| `remove-from-tag` | 从标签删除 | Remove from tag |
| `task-info` | 任务信息 | Task info |
| `task-results` | 任务结果 | Task results |
| `cancel-task` | 取消任务 | Cancel task |
| `user-info` | 用户信息 | User info |
| `user-permissions` | 用户权限 | User permissions |

---

## 最佳实践 | Best Practices

### 1. 构建前检查 | Pre-build Checks
- 确保 spec 文件符合打包规范
- Ensure spec file follows packaging guidelines
- 在本地 mock 环境中测试构建
- Test build in local mock environment

### 2. 标签策略 | Tag Strategy
- 使用标准标签命名（如 f39, f39-updates）
- Use standard tag naming
- 正确配置标签继承
- Configure tag inheritance correctly

### 3. 错误处理 | Error Handling
- 检查构建失败原因
- Check build failure reasons
- 查看完整构建日志
- View complete build logs

---

## 故障排除 | Troubleshooting

### 认证失败 | Authentication Failed
```bash
# 检查 KRB5 票据
# Check KRB5 ticket
klist

# 刷新票据
# Refresh ticket
kinit username@FEDORAPROJECT.ORG
```

### 构建失败 | Build Failed
```bash
# 查看构建日志
# View build logs
koji build-logs 123456

# 重试构建
# Retry build
koji retry-build 123456
```

---

## 参考资料 | References

- [Koji 官方文档 | Koji Official Docs](https://koji.fedoraproject.org/docs/)
- [Fedora 打包指南 | Fedora Packaging Guide](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [DistGit 文档 | DistGit Docs](https://src.fedoraproject.org/)

---

## 许可证 | License

MIT License

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-23)
- 初始版本，完整的 Koji API 支持
- Initial release with full Koji API coverage
- 中英文双语文档
- Bilingual documentation (Chinese/English)
