# 51find-scrapy
```sql
CREATE TABLE `cd_cnblogs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` char(32) NOT NULL COMMENT 'url md5编码id',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `description` varchar(1024) DEFAULT NULL COMMENT '描述',
  `link` varchar(255) DEFAULT NULL COMMENT 'url链接',
  `list_url` varchar(255) DEFAULT NULL COMMENT '分页url链接',
  `create_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  `modify_time` datetime DEFAULT NULL COMMENT 'modify time',
  `post_time` datetime DEFAULT NULL COMMENT 'article post time',
  `post_author` varchar(32) DEFAULT NULL COMMENT 'post author name',
  `view_count` int(11) unsigned DEFAULT '0' COMMENT 'view count',
  `comment_count` int(11) DEFAULT '0' COMMENT 'comment_count',
  PRIMARY KEY (`id`),
  UNIQUE KEY `itemid` (`item_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
```
