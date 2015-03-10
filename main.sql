/*
Navicat SQLite Data Transfer

Source Server         : stock_system
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2015-03-06 14:15:24
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_group";
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(80) NOT NULL UNIQUE);

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_group_permissions";
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"), UNIQUE ("group_id", "permission_id"));

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_permission";
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"), "codename" varchar(100) NOT NULL, UNIQUE ("content_type_id", "codename"));

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_user";
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NOT NULL, "is_superuser" bool NOT NULL, "username" varchar(30) NOT NULL UNIQUE, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL, "email" varchar(75) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL);

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_user_groups";
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "group_id" integer NOT NULL REFERENCES "auth_group" ("id"), UNIQUE ("user_id", "group_id"));

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_user_user_permissions";
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"), UNIQUE ("user_id", "permission_id"));

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_admin_log";
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id"), "user_id" integer NOT NULL REFERENCES "auth_user" ("id"));

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_content_type";
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL, UNIQUE ("app_label", "model"));

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_migrations";
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_session";
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

-- ----------------------------
-- Table structure for order_contact_info
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_contact_info";
CREATE TABLE "order_contact_info" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address" varchar(30) NOT NULL, "phone_number" varchar(20) NOT NULL, "customer_id" integer NOT NULL REFERENCES "order_customer" ("id"));

-- ----------------------------
-- Table structure for order_customer
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_customer";
CREATE TABLE "order_customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sex" bool NOT NULL, "name" varchar(100) NOT NULL, "level_id" integer NOT NULL REFERENCES "order_customer_level" ("id"));

-- ----------------------------
-- Table structure for order_customer_level
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_customer_level";
CREATE TABLE "order_customer_level" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "level" integer NOT NULL);

-- ----------------------------
-- Table structure for order_order
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_order";
CREATE TABLE "order_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "delivery_no" varchar(30) NOT NULL, "fact_money" decimal NOT NULL, "customer_id" integer NOT NULL REFERENCES "order_customer" ("id"), "issuing_person_id" integer NOT NULL REFERENCES "role_issuing_person" ("id"), "product_id" integer NOT NULL REFERENCES "order_product" ("id"), "state_id" integer NOT NULL REFERENCES "order_order_state" ("id"));

-- ----------------------------
-- Table structure for order_order_state
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_order_state";
CREATE TABLE "order_order_state" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);

-- ----------------------------
-- Table structure for order_product
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_product";
CREATE TABLE "order_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "price" decimal NOT NULL, "delivery_type" varchar(100) NOT NULL);

-- ----------------------------
-- Table structure for order_stock_product
-- ----------------------------
DROP TABLE IF EXISTS "main"."order_stock_product";
CREATE TABLE "order_stock_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" decimal NOT NULL, "delivery_bill" bool NOT NULL, "product_id" integer NOT NULL REFERENCES "order_product" ("id"), "stock_id" integer NOT NULL REFERENCES "stock_stock" ("id"));

-- ----------------------------
-- Table structure for role_issuing_person
-- ----------------------------
DROP TABLE IF EXISTS "main"."role_issuing_person";
CREATE TABLE "role_issuing_person" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);

-- ----------------------------
-- Table structure for role_userprofile
-- ----------------------------
DROP TABLE IF EXISTS "main"."role_userprofile";
CREATE TABLE "role_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "role" integer NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id"));

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "main"."sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Table structure for stock_stock
-- ----------------------------
DROP TABLE IF EXISTS "main"."stock_stock";
CREATE TABLE "stock_stock" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "detail" varchar(100) NOT NULL, "price" decimal NOT NULL, "quantity" integer NOT NULL, "stock_channel_id" integer NOT NULL REFERENCES "stock_stock_channel" ("id"), "stock_type_id" integer NOT NULL REFERENCES "stock_stock_type" ("id"));

-- ----------------------------
-- Table structure for stock_stock_channel
-- ----------------------------
DROP TABLE IF EXISTS "main"."stock_stock_channel";
CREATE TABLE "stock_stock_channel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "company" varchar(100) NOT NULL, "person" varchar(50) NOT NULL, "phone_number" varchar(20) NOT NULL);

-- ----------------------------
-- Table structure for stock_stock_management
-- ----------------------------
DROP TABLE IF EXISTS "main"."stock_stock_management";
CREATE TABLE "stock_stock_management" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "stock_mode" bool NOT NULL, "mode_id" integer NOT NULL REFERENCES "stock_stock_mode" ("id"), "stock_id" integer NOT NULL REFERENCES "stock_stock" ("id"));

-- ----------------------------
-- Table structure for stock_stock_mode
-- ----------------------------
DROP TABLE IF EXISTS "main"."stock_stock_mode";
CREATE TABLE "stock_stock_mode" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "method" varchar(200) NOT NULL, "description" varchar(100) NOT NULL);

-- ----------------------------
-- Table structure for stock_stock_type
-- ----------------------------
DROP TABLE IF EXISTS "main"."stock_stock_type";
CREATE TABLE "stock_stock_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type_name" varchar(50) NOT NULL);

-- ----------------------------
-- Indexes structure for table auth_group_permissions
-- ----------------------------
CREATE INDEX "main"."auth_group_permissions_0e939a4f"
ON "auth_group_permissions" ("group_id" ASC);
CREATE INDEX "main"."auth_group_permissions_8373b171"
ON "auth_group_permissions" ("permission_id" ASC);

-- ----------------------------
-- Indexes structure for table auth_permission
-- ----------------------------
CREATE INDEX "main"."auth_permission_417f1b1c"
ON "auth_permission" ("content_type_id" ASC);

-- ----------------------------
-- Indexes structure for table auth_user_groups
-- ----------------------------
CREATE INDEX "main"."auth_user_groups_0e939a4f"
ON "auth_user_groups" ("group_id" ASC);
CREATE INDEX "main"."auth_user_groups_e8701ad4"
ON "auth_user_groups" ("user_id" ASC);

-- ----------------------------
-- Indexes structure for table auth_user_user_permissions
-- ----------------------------
CREATE INDEX "main"."auth_user_user_permissions_8373b171"
ON "auth_user_user_permissions" ("permission_id" ASC);
CREATE INDEX "main"."auth_user_user_permissions_e8701ad4"
ON "auth_user_user_permissions" ("user_id" ASC);

-- ----------------------------
-- Indexes structure for table django_admin_log
-- ----------------------------
CREATE INDEX "main"."django_admin_log_417f1b1c"
ON "django_admin_log" ("content_type_id" ASC);
CREATE INDEX "main"."django_admin_log_e8701ad4"
ON "django_admin_log" ("user_id" ASC);

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "main"."django_session_de54fa62"
ON "django_session" ("expire_date" ASC);

-- ----------------------------
-- Indexes structure for table order_contact_info
-- ----------------------------
CREATE INDEX "main"."order_contact_info_cb24373b"
ON "order_contact_info" ("customer_id" ASC);

-- ----------------------------
-- Indexes structure for table order_customer
-- ----------------------------
CREATE INDEX "main"."order_customer_80e0bd5f"
ON "order_customer" ("level_id" ASC);

-- ----------------------------
-- Indexes structure for table order_order
-- ----------------------------
CREATE INDEX "main"."order_order_98beda94"
ON "order_order" ("issuing_person_id" ASC);
CREATE INDEX "main"."order_order_9bea82de"
ON "order_order" ("product_id" ASC);
CREATE INDEX "main"."order_order_cb24373b"
ON "order_order" ("customer_id" ASC);
CREATE INDEX "main"."order_order_d5582625"
ON "order_order" ("state_id" ASC);

-- ----------------------------
-- Indexes structure for table order_stock_product
-- ----------------------------
CREATE INDEX "main"."order_stock_product_9bea82de"
ON "order_stock_product" ("product_id" ASC);
CREATE INDEX "main"."order_stock_product_aff86b81"
ON "order_stock_product" ("stock_id" ASC);

-- ----------------------------
-- Indexes structure for table stock_stock
-- ----------------------------
CREATE INDEX "main"."stock_stock_3a46d5e0"
ON "stock_stock" ("stock_type_id" ASC);
CREATE INDEX "main"."stock_stock_4cf4f30f"
ON "stock_stock" ("stock_channel_id" ASC);

-- ----------------------------
-- Indexes structure for table stock_stock_management
-- ----------------------------
CREATE INDEX "main"."stock_stock_management_aff86b81"
ON "stock_stock_management" ("stock_id" ASC);
CREATE INDEX "main"."stock_stock_management_fb57d014"
ON "stock_stock_management" ("mode_id" ASC);
