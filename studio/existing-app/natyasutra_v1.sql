-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 20, 2026 at 03:40 PM
-- Server version: 5.7.20
-- PHP Version: 7.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `natyasutra_v1`
--

-- --------------------------------------------------------

--
-- Table structure for table `ci_sessions`
--

CREATE TABLE `ci_sessions` (
  `id` varchar(128) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `timestamp` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `data` blob NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `id` int(11) NOT NULL,
  `item_number` varchar(255) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `payment_status` varchar(255) NOT NULL,
  `payment_amount` double(10,2) NOT NULL,
  `payment_currency` varchar(255) NOT NULL,
  `txn_id` varchar(255) NOT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `student_login_attempt_failed`
--

CREATE TABLE `student_login_attempt_failed` (
  `id` bigint(11) NOT NULL,
  `username` text NOT NULL,
  `ip` text NOT NULL,
  `user_agent` text NOT NULL,
  `date_time` datetime NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_admin`
--

CREATE TABLE `tb_admin` (
  `id` int(11) NOT NULL,
  `name` text,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `user_type` tinyint(4) NOT NULL COMMENT '1-Superadmin, 2-Director, 3-Accounts',
  `email` text,
  `accessible_menus` text,
  `redirect_menu` int(11) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_banner`
--

CREATE TABLE `tb_banner` (
  `id` int(11) NOT NULL,
  `title` text CHARACTER SET utf8,
  `sub_title` text CHARACTER SET utf8,
  `sub_title_2` text,
  `image` text,
  `web_banner_image` text,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `destination_type` tinyint(4) DEFAULT NULL COMMENT '1-category, 2-Guru, 3-Class, 4-External Link',
  `destination_id` bigint(20) DEFAULT NULL,
  `destination_external_link` text,
  `destination_target` tinyint(4) DEFAULT NULL COMMENT '1-same tab, 2-new tab',
  `display_type` int(11) DEFAULT NULL COMMENT '1-image,2-video',
  `web_video_file` text,
  `video_file` text,
  `added_on` datetime DEFAULT NULL,
  `added_by` bigint(20) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` bigint(20) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` bigint(20) DEFAULT NULL,
  `deleted_by_ip` text,
  `status` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_cart`
--

CREATE TABLE `tb_cart` (
  `id` bigint(20) NOT NULL,
  `transaction_number` text NOT NULL,
  `session_id` text NOT NULL,
  `item_type` tinyint(4) NOT NULL COMMENT '1-programme, 2- video,3- music subscription,4-individual album',
  `item_id` bigint(20) NOT NULL,
  `price_in_inr` decimal(10,2) DEFAULT NULL,
  `price_in_usd` decimal(10,2) DEFAULT NULL,
  `required_participation` tinyint(4) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `cost_id` bigint(20) NOT NULL,
  `old_purchase_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_category`
--

CREATE TABLE `tb_category` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `display_name` text,
  `parent_id` int(11) NOT NULL,
  `description` text,
  `banner_description` text,
  `display_order` int(11) NOT NULL,
  `mudra_image` text,
  `mudra_text1` text,
  `mudra_text2` text,
  `thumb_image` text,
  `share_img` text,
  `detailed_page_image` text,
  `quotes` text,
  `status` int(11) NOT NULL,
  `filename` text,
  `meta_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_category_cover_images`
--

CREATE TABLE `tb_category_cover_images` (
  `id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL COMMENT 'id from tb_category',
  `cover_image` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-Active,2-delete',
  `added_ip` text,
  `added_by` text,
  `added_on` datetime DEFAULT NULL,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` text,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` text,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_certificate_download`
--

CREATE TABLE `tb_certificate_download` (
  `id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  `student_name` text CHARACTER SET utf8,
  `purchase_id` bigint(20) NOT NULL,
  `downloaded_on` datetime NOT NULL,
  `downloaded_ip` text,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_class_music_payment`
--

CREATE TABLE `tb_class_music_payment` (
  `id` bigint(20) NOT NULL,
  `project_id` bigint(20) NOT NULL,
  `artiste_id` bigint(20) NOT NULL,
  `paid_artist_type` enum('g','a') NOT NULL DEFAULT 'a',
  `paid_to_id` bigint(20) NOT NULL,
  `amount` bigint(20) NOT NULL,
  `paid_date` date NOT NULL,
  `bank_id` bigint(20) NOT NULL,
  `remarks` text,
  `status` tinyint(4) NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_by` bigint(20) DEFAULT NULL,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_collection`
--

CREATE TABLE `tb_collection` (
  `id` int(11) NOT NULL,
  `title` text CHARACTER SET utf8,
  `short_description` text CHARACTER SET utf8,
  `description` text CHARACTER SET utf8,
  `home_page_image` text CHARACTER SET utf8,
  `share_img` text CHARACTER SET utf8,
  `banner_img` text CHARACTER SET utf8,
  `alt_value` text CHARACTER SET utf8,
  `initial_view_count` int(11) DEFAULT NULL,
  `actual_view_count` int(11) NOT NULL,
  `average_rating` float DEFAULT NULL,
  `rate_1` int(11) NOT NULL,
  `rate_2` int(11) NOT NULL,
  `rate_3` int(11) NOT NULL,
  `rate_4` int(11) NOT NULL,
  `rate_5` int(11) NOT NULL,
  `int_rate_1` int(11) NOT NULL,
  `int_rate_2` int(11) NOT NULL,
  `int_rate_3` int(11) NOT NULL,
  `int_rate_4` int(11) NOT NULL,
  `int_rate_5` int(11) NOT NULL,
  `cost_type` int(11) NOT NULL COMMENT '1- free , 2- paid,3- long term',
  `visible_platform` int(11) NOT NULL COMMENT '1- desktop,2-mobile,3-both',
  `status` int(11) DEFAULT NULL COMMENT '0-private,1-public,2-deleted',
  `filename` text,
  `meta_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `home_view_status` enum('n','y') DEFAULT 'n',
  `added_on` datetime DEFAULT NULL,
  `published_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_common_settings`
--

CREATE TABLE `tb_common_settings` (
  `id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL COMMENT '1-pgm banner, 2- pgm cover,3- video custom thumb,4-share image,5-Profile Image,6- Coupon Advertisment, 7- Banner image, 8- profile thumb image, 9- Latest updates image, 10- Dance form page image, 16 - artist profile, 18-home page thumb image for dance section, 30-Home page banner web image, 31-Home page banner mobile image, 32-Home page banner web video, 33-Home page banner mobile video',
  `description` text NOT NULL,
  `size` int(11) DEFAULT '0' COMMENT 'in mb',
  `width` int(11) DEFAULT '0' COMMENT 'in px',
  `height` int(11) DEFAULT '0' COMMENT 'in px',
  `file_format` text,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_cost_package`
--

CREATE TABLE `tb_cost_package` (
  `id` int(11) NOT NULL,
  `title` text,
  `cost_type` enum('f','r') NOT NULL DEFAULT 'f' COMMENT 'f-Fresh, r-renewal',
  `item_id` int(11) NOT NULL COMMENT 'id from tb_video or tb_programme',
  `item_type` enum('1','2') NOT NULL COMMENT '1-programme,2-video',
  `video_track_type_id` smallint(6) DEFAULT NULL,
  `price_in_inr` int(11) DEFAULT NULL,
  `price_in_euro` int(11) DEFAULT NULL,
  `price_in_usd` int(11) DEFAULT NULL,
  `valid_days` int(11) DEFAULT NULL COMMENT 'No: of days/month/year',
  `valid_type` int(11) DEFAULT NULL COMMENT '1-day,2-month,3-year',
  `renew_before` int(11) DEFAULT NULL COMMENT 'in days',
  `status` int(11) NOT NULL COMMENT '1-active, 2- inactive, 3- deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_countries`
--

CREATE TABLE `tb_countries` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `alpha_2` varchar(2) NOT NULL DEFAULT '',
  `alpha_3` varchar(3) NOT NULL DEFAULT '',
  `status` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tb_coupon`
--

CREATE TABLE `tb_coupon` (
  `id` int(11) NOT NULL,
  `title` text,
  `coupon_for` tinyint(4) NOT NULL COMMENT '0-For public, 1-exists in the software',
  `description` text,
  `coupon_code` text NOT NULL,
  `advt_img` text,
  `discount_type` int(11) NOT NULL COMMENT '1-percentage,2-fixed price',
  `dis_per_inr` int(11) DEFAULT NULL,
  `dis_upto_inr` int(11) DEFAULT NULL,
  `dis_per_usd` int(11) DEFAULT NULL,
  `dis_upto_usd` int(11) DEFAULT NULL,
  `dis_amt_inr` int(11) DEFAULT NULL,
  `dis_amt_usd` int(11) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `valid_for` int(11) DEFAULT NULL,
  `collection_id` bigint(20) NOT NULL,
  `no_classes` int(11) NOT NULL COMMENT '0-Range, 1-Fixed Count',
  `from_range` int(11) NOT NULL,
  `to_range` int(11) NOT NULL,
  `class_count` int(11) NOT NULL,
  `video_track_type_id` int(11) NOT NULL,
  `subscription_validity` int(11) NOT NULL,
  `validity_type` tinyint(4) NOT NULL COMMENT '1-day, 2-month, 3-year',
  `uses_per_coupon` int(11) NOT NULL,
  `uses_per_customer` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_coupon_link`
--

CREATE TABLE `tb_coupon_link` (
  `id` int(11) NOT NULL,
  `coupon_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `item_type` int(11) DEFAULT NULL COMMENT '1-programme ,2-video',
  `cost_package_id` int(11) NOT NULL COMMENT 'tb_cost_package',
  `status` int(11) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_coupon_student_link`
--

CREATE TABLE `tb_coupon_student_link` (
  `id` bigint(20) NOT NULL,
  `coupon_id` bigint(20) DEFAULT NULL,
  `student_id` bigint(20) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_delivery_address`
--

CREATE TABLE `tb_delivery_address` (
  `id` int(11) NOT NULL,
  `student_id` bigint(20) DEFAULT NULL,
  `name` text,
  `address` text,
  `countrycode` text,
  `mobile_number` text,
  `country_id` int(11) DEFAULT NULL,
  `state_text` text,
  `city` text,
  `pincode` text,
  `landmark` text,
  `alternate_phone` text,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active, 2- deleted',
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_delivery_details`
--

CREATE TABLE `tb_delivery_details` (
  `id` bigint(20) NOT NULL,
  `delivery_date` varchar(250) DEFAULT NULL,
  `drv_img` text,
  `purchase_id` int(11) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` tinyint(4) DEFAULT NULL,
  `added_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_editor_images`
--

CREATE TABLE `tb_editor_images` (
  `id` bigint(20) NOT NULL,
  `filename` text NOT NULL,
  `dimensions` text NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_faq`
--

CREATE TABLE `tb_faq` (
  `id` int(11) NOT NULL,
  `programme_id` int(11) DEFAULT NULL,
  `video_id` int(11) DEFAULT NULL,
  `question` text,
  `answer` text,
  `status` int(11) NOT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_feedback`
--

CREATE TABLE `tb_feedback` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `user_type` int(11) NOT NULL,
  `email` text NOT NULL,
  `countrycode` text,
  `mobile` text NOT NULL,
  `country` int(11) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `province` text,
  `address` text NOT NULL,
  `age` int(11) NOT NULL,
  `gender` int(11) NOT NULL,
  `mail_lst` int(11) NOT NULL,
  `class` int(11) NOT NULL,
  `comments` text,
  `image` text,
  `url` text,
  `suggestion` text,
  `status` int(11) NOT NULL,
  `reply_text` text,
  `reply_status` tinyint(4) DEFAULT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL,
  `deleted_by` int(11) NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by_ip` text NOT NULL,
  `updated_by` text,
  `updated_by_ip` text,
  `updated_on` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_feedback_class`
--

CREATE TABLE `tb_feedback_class` (
  `id` bigint(20) NOT NULL,
  `feedback_id` int(11) NOT NULL,
  `type` enum('d','p','m') DEFAULT NULL,
  `class_id` int(11) NOT NULL COMMENT 'id from tb_programme',
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_feedback_interests`
--

CREATE TABLE `tb_feedback_interests` (
  `id` bigint(20) NOT NULL,
  `feedback_id` int(11) NOT NULL,
  `type` enum('d','p','m') DEFAULT NULL,
  `category_id` int(11) NOT NULL COMMENT 'id from tb_category',
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_feedback_topics`
--

CREATE TABLE `tb_feedback_topics` (
  `id` bigint(20) NOT NULL,
  `feedback_id` int(11) NOT NULL,
  `type` enum('d','p','m') DEFAULT NULL,
  `category_id` int(11) NOT NULL COMMENT 'id from tb_category',
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_freeclass`
--

CREATE TABLE `tb_freeclass` (
  `id` int(11) NOT NULL,
  `title` text CHARACTER SET utf8,
  `guru_id` int(11) DEFAULT NULL COMMENT 'id from tb_guru_basics',
  `guru_text` text,
  `category_id` int(11) DEFAULT NULL COMMENT 'id fron tb_category',
  `category_text` text,
  `short_description` text CHARACTER SET utf8,
  `description` text CHARACTER SET utf8,
  `home_page_image` text,
  `share_img` text CHARACTER SET utf8,
  `banner_img` text,
  `alt_value` text CHARACTER SET utf8,
  `cover_image` text CHARACTER SET utf8,
  `initial_view_count` int(11) NOT NULL,
  `actual_view_count` int(11) NOT NULL,
  `average_rating` float DEFAULT NULL,
  `rate_1` int(11) NOT NULL,
  `rate_2` int(11) NOT NULL,
  `rate_3` int(11) NOT NULL,
  `rate_4` int(11) NOT NULL,
  `rate_5` int(11) NOT NULL,
  `int_rate_1` int(11) NOT NULL,
  `int_rate_2` int(11) NOT NULL,
  `int_rate_3` int(11) NOT NULL,
  `int_rate_4` int(11) NOT NULL,
  `int_rate_5` int(11) NOT NULL,
  `visible_platform` int(11) NOT NULL COMMENT '1- desktop,2-mobile,3-both',
  `status` int(11) DEFAULT NULL COMMENT '0-private,1-public,2-deleted',
  `filename` text,
  `meta_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_freevideo`
--

CREATE TABLE `tb_freevideo` (
  `id` int(11) NOT NULL,
  `free_class_id` int(11) NOT NULL,
  `title` text CHARACTER SET utf8,
  `video_type` tinyint(4) DEFAULT NULL COMMENT '1-Trailer, 2-Actual video',
  `video_embed_code` text,
  `video_source` enum('1','2') DEFAULT NULL COMMENT '1- youtube ,2-vimeo',
  `custom_video_thumb` text,
  `display_order` int(11) NOT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text,
  `status` int(11) DEFAULT NULL COMMENT '0-private,1-public,2-deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_guru_art_forms`
--

CREATE TABLE `tb_guru_art_forms` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL COMMENT 'id from tb_guru_basics',
  `category_id` int(11) NOT NULL COMMENT 'id from tb_category',
  `profile_image_name` text,
  `profile_video_embed_code` text,
  `video_source` enum('1','2') DEFAULT NULL COMMENT '1- youtube ,2- vimeo',
  `custom_video_thumb` text,
  `status` int(11) NOT NULL COMMENT '1-active, 2- inactive, 3- deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_guru_bank`
--

CREATE TABLE `tb_guru_bank` (
  `id` bigint(20) NOT NULL,
  `guru_id` bigint(20) NOT NULL,
  `is_other_artist` enum('y','n') NOT NULL DEFAULT 'n',
  `guru_name` text,
  `account_number` text NOT NULL,
  `name` text NOT NULL,
  `branch_name` text NOT NULL,
  `ifscode` text NOT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_ip` text,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by_ip` text,
  `status` tinyint(4) NOT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_guru_basics`
--

CREATE TABLE `tb_guru_basics` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `revenue_from` date DEFAULT NULL,
  `display_home_page` enum('y','n') NOT NULL DEFAULT 'y',
  `sernior_artist` enum('y','n') NOT NULL DEFAULT 'n',
  `signature_img` text,
  `portfolio` text,
  `email_id` text,
  `mobile` text,
  `whatsapp_number` text,
  `website` text,
  `address` text,
  `short_description` text,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `profile_image` text,
  `share_image` text,
  `banner_image` text,
  `status` int(11) NOT NULL COMMENT '0- Private,1-Public,2-Deleted',
  `filename` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_guru_description`
--

CREATE TABLE `tb_guru_description` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL,
  `title` text CHARACTER SET utf8 NOT NULL,
  `image` text,
  `description` longtext CHARACTER SET utf8 NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_guru_social_links`
--

CREATE TABLE `tb_guru_social_links` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL COMMENT 'id from tb_guru_basics',
  `social_type` int(11) NOT NULL COMMENT '1-youtube,2-fb,3-tw,4-g+,5-instagram,6-vimeo',
  `social_url` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '1-active , 2-inactive'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_language`
--

CREATE TABLE `tb_language` (
  `id` smallint(6) NOT NULL,
  `name` text NOT NULL,
  `status` tinyint(4) NOT NULL COMMENT '0-private, 1-public, 2-deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_latest_updates`
--

CREATE TABLE `tb_latest_updates` (
  `id` int(11) NOT NULL,
  `title` text,
  `type_id` int(11) NOT NULL COMMENT '1-latest Updates, 2 -Media(id from tb_announcement_type',
  `home_view_status` enum('y','n') NOT NULL DEFAULT 'y',
  `hyperlink` text,
  `description` longtext,
  `short_description` longtext,
  `file_upload` text,
  `guru_id` int(11) DEFAULT NULL,
  `programme_id` bigint(20) DEFAULT NULL,
  `pgm_type` enum('d','p','m','c') DEFAULT NULL,
  `share_image` text,
  `cover_image` text NOT NULL,
  `image_caption` text,
  `alt_value` text,
  `media_date` date DEFAULT NULL,
  `newspaper` text,
  `media_file` text,
  `website_url` text,
  `target_type` int(11) DEFAULT NULL COMMENT '1-same,2 -new ',
  `status` int(11) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text,
  `filename` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_level`
--

CREATE TABLE `tb_level` (
  `id` int(11) NOT NULL,
  `name` text,
  `status` tinyint(4) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_level_sub`
--

CREATE TABLE `tb_level_sub` (
  `id` int(11) NOT NULL,
  `name` text,
  `filename` text,
  `status` tinyint(4) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_marital_status`
--

CREATE TABLE `tb_marital_status` (
  `id` bigint(20) NOT NULL,
  `name` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive, 1-active'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_menu`
--

CREATE TABLE `tb_menu` (
  `id` int(11) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `name` text NOT NULL,
  `menu_session` int(11) NOT NULL COMMENT '1=dance, 2=music',
  `menu_type` int(11) NOT NULL COMMENT '1-Reports, 2-Dance, 3-Music, 4-Products, 5-Culture, 6-Nature, 8-Events, 9-Students, 10-Galleries, 11-General',
  `admin_view_name` text NOT NULL,
  `type` tinyint(4) NOT NULL COMMENT '1=main menu, 2= child menu',
  `parent_id` int(11) NOT NULL COMMENT 'if its a submenu the parent id shows here',
  `url` text NOT NULL,
  `fa_icon` text NOT NULL,
  `open_in` int(11) NOT NULL COMMENT '1- same tab, 2- new tab',
  `active_name` text,
  `status` int(11) NOT NULL,
  `display_order` int(11) NOT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_by_ip` text,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='for backend';

-- --------------------------------------------------------

--
-- Table structure for table `tb_mobile_country_codes`
--

CREATE TABLE `tb_mobile_country_codes` (
  `id` int(11) NOT NULL,
  `country` varchar(148) DEFAULT NULL,
  `short_code` varchar(12) DEFAULT NULL,
  `code` varchar(21) DEFAULT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music`
--

CREATE TABLE `tb_music` (
  `id` bigint(20) NOT NULL,
  `item_type` tinyint(4) NOT NULL COMMENT '1-programme, 2-video',
  `item_id` bigint(20) NOT NULL,
  `title` text CHARACTER SET utf8 NOT NULL,
  `url` text CHARACTER SET utf8 NOT NULL,
  `duration` text COMMENT 'h:i:s format',
  `cost_type` tinyint(4) NOT NULL COMMENT '1-Free, 2-Paid, 3-One Time',
  `added_on` datetime NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_ip` text NOT NULL,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text,
  `status` tinyint(4) NOT NULL COMMENT ' 	0-private,1-public,2-deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_album`
--

CREATE TABLE `tb_music_album` (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8 NOT NULL,
  `category_id` int(11) NOT NULL,
  `produced_by` bigint(20) DEFAULT NULL,
  `album_type` enum('f','p') DEFAULT NULL COMMENT 'free/ paid',
  `individual_purchase` enum('y','n') DEFAULT NULL,
  `subscription` enum('y','n') DEFAULT NULL,
  `short_description` text CHARACTER SET utf8,
  `description` text CHARACTER SET utf8,
  `banner_image` text CHARACTER SET utf8,
  `share_image` text CHARACTER SET utf8,
  `cover_image` text CHARACTER SET utf8,
  `alttag` text,
  `released_on` date DEFAULT NULL,
  `revenue_share` enum('y','n') DEFAULT NULL,
  `initial_view_count` int(11) DEFAULT NULL,
  `int_rate_1` int(11) DEFAULT NULL,
  `int_rate_2` int(11) DEFAULT NULL,
  `int_rate_3` int(11) DEFAULT NULL,
  `int_rate_4` int(11) DEFAULT NULL,
  `int_rate_5` int(11) DEFAULT NULL,
  `average_rating` float DEFAULT NULL,
  `filename` text,
  `meta_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `added_on` datetime NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_from_ip` text NOT NULL,
  `last_modified_on` datetime DEFAULT NULL,
  `last_modified_by` int(11) DEFAULT NULL,
  `last_modified_from_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_from_ip` text,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_album_artist`
--

CREATE TABLE `tb_music_album_artist` (
  `id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_album_category`
--

CREATE TABLE `tb_music_album_category` (
  `id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_artist`
--

CREATE TABLE `tb_music_artist` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `whatsapp_number` text,
  `website` text,
  `email` text,
  `mobile` text,
  `address` text,
  `short_description` text,
  `description` text,
  `profile_image` text,
  `share_image` text,
  `thumb_image` text,
  `filename` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text,
  `added_on` datetime NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_from_ip` text NOT NULL,
  `last_modified_on` datetime DEFAULT NULL,
  `last_modified_by` int(11) DEFAULT NULL,
  `last_modified_from_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_from_ip` text,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_artist_category`
--

CREATE TABLE `tb_music_artist_category` (
  `id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `music_category_id` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_category`
--

CREATE TABLE `tb_music_category` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `parent_id` int(11) NOT NULL,
  `thumb_image` text,
  `share_image` text,
  `main_image` text,
  `home_menu` enum('y','n') NOT NULL DEFAULT 'y',
  `filename` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text,
  `added_on` datetime NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_from_ip` text NOT NULL,
  `last_modified_on` datetime DEFAULT NULL,
  `last_modified_by` int(11) DEFAULT NULL,
  `last_modified_from_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_from_ip` text,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_list`
--

CREATE TABLE `tb_music_list` (
  `id` bigint(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `playlist_master_id` int(11) NOT NULL COMMENT 'only for type = 1',
  `track_id` int(11) NOT NULL,
  `type` int(11) NOT NULL COMMENT '1= playlist, 2= favourite, 3=queue',
  `session_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `added_on` datetime NOT NULL,
  `added_from_ip` text NOT NULL,
  `status` int(11) NOT NULL,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_package`
--

CREATE TABLE `tb_music_package` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `type` enum('s','i') NOT NULL COMMENT 'subscription, individual',
  `album_id` int(11) DEFAULT NULL COMMENT 'only for type = i',
  `duration` int(11) DEFAULT NULL,
  `duration_type` int(11) DEFAULT NULL COMMENT 'month, year, days',
  `price_in_inr` double NOT NULL,
  `price_in_usd` double NOT NULL,
  `price_in_euro` double NOT NULL,
  `renew_before` int(11) DEFAULT NULL COMMENT 'in days',
  `added_on` datetime NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_from_ip` text NOT NULL,
  `last_modified_on` datetime DEFAULT NULL,
  `last_modified_by` int(11) DEFAULT NULL,
  `last_modified_from_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_from_ip` text,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_playlist_master`
--

CREATE TABLE `tb_music_playlist_master` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `created_from_ip` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_music_track`
--

CREATE TABLE `tb_music_track` (
  `id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `trailer` enum('y','n') NOT NULL DEFAULT 'y',
  `title` text NOT NULL,
  `track_file` text NOT NULL,
  `thumb_image` text,
  `duration` text NOT NULL COMMENT 'h:i:s format',
  `remark` text NOT NULL,
  `popular_track` bigint(20) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_by` int(11) NOT NULL,
  `added_from_ip` text NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by` int(11) NOT NULL,
  `deleted_from_ip` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_other_artist`
--

CREATE TABLE `tb_other_artist` (
  `id` bigint(20) NOT NULL,
  `name` text NOT NULL,
  `status` tinyint(4) NOT NULL,
  `added_by` bigint(20) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_pages`
--

CREATE TABLE `tb_pages` (
  `id` bigint(20) NOT NULL,
  `title` text,
  `description` text,
  `collection_id` bigint(20) DEFAULT NULL,
  `parent_id` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `youtube_link` text,
  `file_name` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text,
  `share_image` text,
  `cover_image` text,
  `added_on` datetime DEFAULT NULL,
  `added_by` text,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` bigint(20) DEFAULT NULL,
  `last_updated_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` bigint(20) DEFAULT NULL,
  `deleted_ip` text,
  `status` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_pgallery`
--

CREATE TABLE `tb_pgallery` (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8 NOT NULL,
  `gita_govinda_page_id` bigint(20) NOT NULL,
  `seperate_page` enum('y','n') NOT NULL DEFAULT 'n' COMMENT 'Seperate page for each photos of gallery',
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `short_descr` text CHARACTER SET utf8 NOT NULL,
  `description` text CHARACTER SET utf8 NOT NULL,
  `guru_id` int(11) NOT NULL,
  `display_in` enum('a','g','b','e','c') DEFAULT NULL COMMENT 'a-ony in guru''s page, g-only in gallery page, b-both guru''s page and gallery page, e-gita govinda page, c-both gita govinda and gallery page',
  `display_order` int(11) NOT NULL,
  `file_name` text CHARACTER SET utf8 NOT NULL,
  `page_title` text CHARACTER SET utf8 NOT NULL,
  `meta_keywords` text CHARACTER SET utf8 NOT NULL,
  `meta_description` text CHARACTER SET utf8 NOT NULL,
  `noindex` enum('y','n') NOT NULL DEFAULT 'n',
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_by_ip` text NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_on` datetime NOT NULL,
  `updated_by_ip` text NOT NULL,
  `deleted_by` int(11) NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by_ip` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active,2-deleted,3-archieved'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_picture`
--

CREATE TABLE `tb_picture` (
  `id` int(11) NOT NULL,
  `pgallery_id` int(11) NOT NULL,
  `p_caption` varchar(250) CHARACTER SET utf8 NOT NULL,
  `description` text CHARACTER SET utf8,
  `image_name` text CHARACTER SET utf8 NOT NULL,
  `large_image` text CHARACTER SET utf8,
  `display_order` int(11) NOT NULL,
  `cover_display` enum('y','n') DEFAULT NULL,
  `file_name` text CHARACTER SET utf8,
  `page_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_by_ip` text NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_on` datetime NOT NULL,
  `updated_by_ip` text NOT NULL,
  `deleted_by` int(11) NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by_ip` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active,2-deleted,3-archieved'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_producer`
--

CREATE TABLE `tb_producer` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product`
--

CREATE TABLE `tb_product` (
  `id` bigint(20) NOT NULL,
  `p_code` text,
  `name` text,
  `category_id` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `weight_in` tinyint(4) DEFAULT NULL COMMENT '1- gm, 2- Kg',
  `breadth` int(11) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `dimention_in` int(11) DEFAULT NULL COMMENT '1- cm, 2- m',
  `no_of_pages` int(11) DEFAULT NULL,
  `cover_image` text,
  `share_image` text,
  `related_to_danceform` int(11) DEFAULT NULL,
  `short_description` text,
  `description` text,
  `share_img` text,
  `alt_value` text,
  `initial_view_count` int(11) NOT NULL,
  `actual_view_count` int(11) NOT NULL,
  `average_rating` int(11) NOT NULL,
  `rate_1` int(11) NOT NULL,
  `rate_2` int(11) NOT NULL,
  `rate_3` int(11) NOT NULL,
  `rate_4` int(11) NOT NULL,
  `rate_5` int(11) NOT NULL,
  `int_rate_1` int(11) NOT NULL,
  `int_rate_2` int(11) NOT NULL,
  `int_rate_3` int(11) NOT NULL,
  `int_rate_4` int(11) NOT NULL,
  `int_rate_5` int(11) NOT NULL,
  `visible_platform` tinyint(4) DEFAULT NULL COMMENT '1- desktop,2-mobile,3-both ',
  `home_view_status` enum('y','n') DEFAULT 'n',
  `filename` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text,
  `added_on` datetime DEFAULT NULL,
  `published_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text,
  `status` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product_category`
--

CREATE TABLE `tb_product_category` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `parent_id` int(11) NOT NULL,
  `description` text,
  `thumb_image` text,
  `share_img` text,
  `detailed_page_image` text,
  `status` int(11) NOT NULL,
  `filename` text,
  `meta_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product_cost`
--

CREATE TABLE `tb_product_cost` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `title` bigint(20) DEFAULT NULL,
  `price_in_inr` int(11) NOT NULL,
  `price_in_usd` int(11) NOT NULL,
  `price_in_euro` int(11) DEFAULT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product_delivery`
--

CREATE TABLE `tb_product_delivery` (
  `id` bigint(20) NOT NULL,
  `purchase_id` bigint(20) NOT NULL,
  `delivery_id` bigint(20) NOT NULL,
  `status` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product_description`
--

CREATE TABLE `tb_product_description` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL COMMENT 'id of tb_product',
  `title` text,
  `description` text,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product_image`
--

CREATE TABLE `tb_product_image` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `is_cover_image` enum('y','n') DEFAULT 'n',
  `small_image` text NOT NULL,
  `large_image` text NOT NULL,
  `extra_large_image` text NOT NULL,
  `display_order` int(11) DEFAULT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_product_video`
--

CREATE TABLE `tb_product_video` (
  `id` int(11) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `title` text CHARACTER SET utf8,
  `embed_code` text,
  `video_source` enum('1','2') DEFAULT NULL COMMENT '1- youtube ,2-vimeo',
  `custom_video_thumb` text,
  `display_order` int(11) NOT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text,
  `status` int(11) DEFAULT NULL COMMENT '0-private,1-public,2-deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_programme`
--

CREATE TABLE `tb_programme` (
  `id` int(11) NOT NULL,
  `parent_id` bigint(20) DEFAULT NULL,
  `collection_id` bigint(20) DEFAULT NULL,
  `collection_class_group` tinyint(4) DEFAULT NULL,
  `prepublication` enum('y','n') NOT NULL DEFAULT 'n',
  `is_artform` enum('y','n') NOT NULL DEFAULT 'y',
  `title` text CHARACTER SET utf8,
  `sub_head_1` text,
  `sub_head_2` text,
  `show_price` enum('y','n') NOT NULL DEFAULT 'y',
  `participating_in` tinyint(4) NOT NULL COMMENT '0-Only online, 1-Only offline, 2-Both',
  `venue` text,
  `certificate_title` text CHARACTER SET utf8,
  `language_id` smallint(6) DEFAULT NULL,
  `guru_id` int(11) DEFAULT NULL COMMENT 'id from tb_guru_basics',
  `category_id` int(11) DEFAULT NULL COMMENT 'id fron tb_category',
  `topic_related_category_id` int(11) DEFAULT NULL,
  `level_id` int(11) DEFAULT NULL COMMENT 'id from tb_category_level',
  `level_sub_id` int(11) DEFAULT NULL,
  `dp_level_name` text CHARACTER SET utf8,
  `sub_head` text,
  `tags` text CHARACTER SET utf8,
  `short_description` text CHARACTER SET utf8,
  `description` text CHARACTER SET utf8,
  `webinar_on` date DEFAULT NULL,
  `webinar_to` date DEFAULT NULL,
  `webinar_start_time` text,
  `webinar_end_time` text,
  `webinar_display_upto` datetime DEFAULT NULL,
  `noof_participants` int(11) DEFAULT NULL,
  `revenue_share` enum('y','n') NOT NULL DEFAULT 'y',
  `home_page_image` text CHARACTER SET utf8,
  `share_img` text CHARACTER SET utf8,
  `banner_img` text CHARACTER SET utf8,
  `alt_value` text CHARACTER SET utf8,
  `course_includes` text,
  `what_you_learn` text,
  `requirements` text,
  `cover_image` text CHARACTER SET utf8,
  `music_section_thumb` text CHARACTER SET utf8,
  `initial_view_count` int(11) DEFAULT NULL,
  `actual_view_count` int(11) NOT NULL,
  `average_rating` float DEFAULT NULL,
  `rate_1` int(11) NOT NULL,
  `rate_2` int(11) NOT NULL,
  `rate_3` int(11) NOT NULL,
  `rate_4` int(11) NOT NULL,
  `rate_5` int(11) NOT NULL,
  `int_rate_1` int(11) NOT NULL,
  `int_rate_2` int(11) NOT NULL,
  `int_rate_3` int(11) NOT NULL,
  `int_rate_4` int(11) NOT NULL,
  `int_rate_5` int(11) NOT NULL,
  `cost_type` int(11) NOT NULL COMMENT '1- free , 2- paid,3- long term',
  `visible_platform` int(11) NOT NULL COMMENT '1- desktop,2-mobile,3-both',
  `status` int(11) DEFAULT NULL COMMENT '0-private,1-public,2-deleted',
  `filename` text,
  `meta_title` text CHARACTER SET utf8,
  `meta_keywords` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `home_view_status` enum('n','y') DEFAULT 'n',
  `added_on` datetime DEFAULT NULL,
  `published_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_programme_artist`
--

CREATE TABLE `tb_programme_artist` (
  `id` bigint(20) NOT NULL,
  `programme_id` bigint(20) NOT NULL,
  `guru_id` bigint(20) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_programme_description`
--

CREATE TABLE `tb_programme_description` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL COMMENT 'id of tb_programme or tb_video',
  `item_type` int(11) NOT NULL COMMENT '1- programme, 2-video',
  `title` text CHARACTER SET utf8 NOT NULL,
  `description` text CHARACTER SET utf8 NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_programme_video`
--

CREATE TABLE `tb_programme_video` (
  `id` int(11) NOT NULL,
  `programme_id` int(11) NOT NULL COMMENT 'id from tb_programme',
  `video_id` int(11) NOT NULL COMMENT 'id from tb_video',
  `is_trailor` enum('y','n') NOT NULL DEFAULT 'n',
  `display_order` float DEFAULT NULL,
  `status` int(11) NOT NULL COMMENT '0-private,1-public,2-deleted',
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_project`
--

CREATE TABLE `tb_project` (
  `id` bigint(20) NOT NULL,
  `name` text NOT NULL,
  `status` tinyint(4) NOT NULL,
  `added_by` bigint(20) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_purchase`
--

CREATE TABLE `tb_purchase` (
  `id` int(11) NOT NULL,
  `payment_gateway` varchar(2) NOT NULL COMMENT 'pm-PayUmoney, pp-PayPal, BT-Bank Transfer',
  `exact_payment_gateway` tinyint(4) NOT NULL COMMENT '1-Payumoney, 2-Paypal, 3-Razorpay',
  `offer_type` enum('1','2','3','4') DEFAULT NULL COMMENT '1-coupon , 2-renewal, 3- Both',
  `coupon_id` int(11) DEFAULT NULL COMMENT 'id from tb_renewal',
  `renewal_id` int(11) NOT NULL COMMENT 'id from tb_renewal',
  `voucher_id` int(11) DEFAULT NULL,
  `transaction_number` text NOT NULL,
  `order_id` bigint(20) DEFAULT NULL,
  `razorpay_order_id` text,
  `student_id` int(11) NOT NULL,
  `purchase_from` int(11) NOT NULL COMMENT '0-dance,1-music',
  `transaction_status` int(11) NOT NULL COMMENT '1-initiated,2-proceed to payment getway,3-success,4-failure,6-payment refunded',
  `total_payable_amount` decimal(10,2) NOT NULL,
  `total_payable_amount_usd` decimal(10,2) NOT NULL,
  `actual_amount_inr` double DEFAULT NULL,
  `actual_amount_usd` double DEFAULT NULL,
  `offer_amount_inr` double DEFAULT NULL,
  `offer_amount_usd` double DEFAULT NULL,
  `refund_amount` int(11) DEFAULT NULL,
  `dateof_refund` date DEFAULT NULL,
  `refund_entered_on` datetime DEFAULT NULL,
  `currency_type` int(11) NOT NULL COMMENT '1-INR,2-USD,3-EURO',
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_purchase_items`
--

CREATE TABLE `tb_purchase_items` (
  `id` int(11) NOT NULL,
  `purchase_id` bigint(20) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `offer_type` tinyint(4) NOT NULL COMMENT '1-Coupon',
  `offer_id` bigint(20) NOT NULL,
  `item_id` int(11) NOT NULL COMMENT 'id from tb_video or tb_programme',
  `required_participation` tinyint(4) NOT NULL,
  `item_type` enum('1','2','3','4','5') NOT NULL COMMENT '1-programme,2-video,3- music subscription, 4- individual album purchase, 5- product',
  `quantity` int(11) DEFAULT NULL,
  `cost_package_id` int(11) NOT NULL,
  `cost_type` int(11) DEFAULT NULL COMMENT '2-Subscription, 3-One time Payment',
  `valid_type` int(11) NOT NULL COMMENT '1-day, 2-month, 3-year',
  `actual_price_inr` decimal(10,2) DEFAULT NULL,
  `actual_price_usd` decimal(10,2) DEFAULT NULL,
  `actual_price` decimal(10,2) NOT NULL,
  `offer_amount_inr` decimal(10,2) NOT NULL,
  `offer_amount_usd` decimal(10,2) NOT NULL,
  `payable_amount_inr` decimal(10,2) NOT NULL,
  `payable_amount_usd` decimal(10,2) NOT NULL,
  `payable_amount` decimal(10,2) NOT NULL,
  `valid_days` int(11) DEFAULT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date NOT NULL,
  `renewed_status` int(11) NOT NULL COMMENT '1-yes,2-no',
  `renewal_reminder` enum('y','n') NOT NULL DEFAULT 'n',
  `fetch_status` enum('y','n') NOT NULL DEFAULT 'n',
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_rating_review`
--

CREATE TABLE `tb_rating_review` (
  `id` int(11) NOT NULL,
  `item_id` int(11) DEFAULT NULL,
  `item_type` int(11) DEFAULT NULL COMMENT '1-programme, 2-video',
  `student_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL COMMENT 'rating (1/2/3/4/5)',
  `review` text,
  `review_date_time` datetime NOT NULL,
  `admin_approval` enum('p','a','r') NOT NULL DEFAULT 'p',
  `status` int(11) NOT NULL,
  `added_ip` text,
  `admin_approved_on` datetime DEFAULT NULL,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_revenue_deduction_heads`
--

CREATE TABLE `tb_revenue_deduction_heads` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `after_total_deduction` enum('y','n','g') NOT NULL DEFAULT 'n' COMMENT 'g-duduct from guru''s share',
  `display_order` tinyint(4) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_revenue_generate`
--

CREATE TABLE `tb_revenue_generate` (
  `id` bigint(20) NOT NULL,
  `purchase_item_table_id` bigint(20) NOT NULL,
  `item_id` bigint(20) NOT NULL,
  `guru_id` bigint(20) NOT NULL,
  `guru_id_str` text,
  `amount_from` enum('s','i') DEFAULT NULL,
  `return_type` tinyint(4) NOT NULL COMMENT '0-Lesson, 1- Webinar, 2- Workshop',
  `total_amount` decimal(10,2) NOT NULL,
  `bank_id` int(11) DEFAULT NULL,
  `pyment_ref_no` text,
  `added_on` datetime NOT NULL,
  `exact_added_on` datetime DEFAULT NULL,
  `added_by` bigint(20) NOT NULL,
  `added_by_ip` text NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_revenue_generate_sub`
--

CREATE TABLE `tb_revenue_generate_sub` (
  `id` bigint(20) NOT NULL,
  `revenue_generate_id` bigint(20) NOT NULL,
  `ded_id` bigint(20) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `amount` decimal(10,0) NOT NULL,
  `revenue_settings_id` bigint(20) NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_revenue_settings_new`
--

CREATE TABLE `tb_revenue_settings_new` (
  `id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `item_type` tinyint(4) NOT NULL COMMENT '1-Online class',
  `cost_id` bigint(20) NOT NULL,
  `split_type` enum('p','f') NOT NULL DEFAULT 'p' COMMENT 'p-Percentage, f-Fixed Amount',
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `update_flag` enum('y','n') NOT NULL DEFAULT 'n',
  `added_on` datetime NOT NULL,
  `added_by` bigint(20) NOT NULL,
  `added_ip` text NOT NULL,
  `last_modified_on` datetime NOT NULL,
  `last_modified_by` bigint(20) NOT NULL,
  `last_modified_ip` text NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by` bigint(20) NOT NULL,
  `deleted_ip` text NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_revenue_settings_new_head_split`
--

CREATE TABLE `tb_revenue_settings_new_head_split` (
  `id` bigint(20) NOT NULL,
  `revenue_settings_new_id` bigint(20) NOT NULL,
  `deduction_head_id` bigint(20) NOT NULL,
  `guru_id` bigint(20) NOT NULL,
  `deduction` float NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_shipping_details`
--

CREATE TABLE `tb_shipping_details` (
  `id` bigint(20) NOT NULL,
  `shipping_date` varchar(200) DEFAULT NULL,
  `shipping_number` varchar(200) DEFAULT NULL,
  `purchase_id` int(11) DEFAULT NULL,
  `added_on` datetime DEFAULT NULL,
  `added_by` tinyint(4) DEFAULT NULL,
  `added_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_states`
--

CREATE TABLE `tb_states` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_student`
--

CREATE TABLE `tb_student` (
  `id` int(11) NOT NULL,
  `name` text,
  `gender` enum('m','f','o','n') DEFAULT NULL,
  `gender_other` text,
  `dob` date DEFAULT NULL,
  `email` text NOT NULL,
  `address` text,
  `job` text,
  `marital_status_id` int(11) DEFAULT NULL,
  `md5_email` text NOT NULL,
  `api_token` text,
  `for_activation_date` text NOT NULL,
  `password` text NOT NULL,
  `countrycode` text,
  `mobile_number` text,
  `interest_in` int(11) DEFAULT NULL COMMENT 'id from tb_artform_signup_list',
  `country` text,
  `state_id` int(11) DEFAULT NULL,
  `state_text` text,
  `city` text,
  `pincode` text,
  `registered_date_time` datetime NOT NULL,
  `reference_number` text,
  `profile_img` text,
  `block_cnt` int(11) DEFAULT NULL,
  `register_from` int(11) NOT NULL COMMENT '0-Dance,1-Music ',
  `address_verified` enum('y','n') NOT NULL DEFAULT 'y',
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active, 2- deleted',
  `activation_key` text,
  `verification_code` text,
  `activation_date_time` datetime DEFAULT NULL,
  `activation_ip` text,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_student_interested_categories`
--

CREATE TABLE `tb_student_interested_categories` (
  `id` bigint(20) NOT NULL,
  `student_id` int(11) NOT NULL,
  `type` enum('d','p','m') DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_student_login_log`
--

CREATE TABLE `tb_student_login_log` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL COMMENT 'id from tb_student',
  `login_date_time` datetime DEFAULT NULL,
  `login_ip` text NOT NULL,
  `logout_date_time` datetime DEFAULT NULL,
  `active` enum('a','d') NOT NULL DEFAULT 'd' COMMENT 'a-active,d-deactive'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_student_topic_categories`
--

CREATE TABLE `tb_student_topic_categories` (
  `id` bigint(20) NOT NULL,
  `student_id` int(11) NOT NULL,
  `type` enum('d','p','m') DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_transaction_log`
--

CREATE TABLE `tb_transaction_log` (
  `id` int(11) NOT NULL,
  `purchase_id` int(11) NOT NULL,
  `transaction_status` int(11) NOT NULL,
  `log_date_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_vgallery`
--

CREATE TABLE `tb_vgallery` (
  `id` bigint(20) NOT NULL,
  `name` text CHARACTER SET utf8 NOT NULL,
  `gita_govinda_page_id` bigint(20) DEFAULT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `display_in` enum('a','g','b','e','c') DEFAULT NULL COMMENT 'a-ony in guru''s page, g-gallery only, b-both, e-gita govinda page, c-both gita govinda and gallery page',
  `short_descr` text CHARACTER SET utf8 NOT NULL,
  `description` text CHARACTER SET utf8 NOT NULL,
  `display_order` int(11) NOT NULL,
  `event_related` enum('y','n') NOT NULL,
  `event_id` int(11) NOT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `home_page_image` text CHARACTER SET utf8,
  `file_name` text CHARACTER SET utf8 NOT NULL,
  `page_title` text CHARACTER SET utf8 NOT NULL,
  `meta_keywords` text CHARACTER SET utf8 NOT NULL,
  `meta_description` text CHARACTER SET utf8 NOT NULL,
  `noindex` enum('y','n') NOT NULL DEFAULT 'n',
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_by_ip` text NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_on` date NOT NULL,
  `updated_by_ip` text NOT NULL,
  `deleted_by` int(11) NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by_ip` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active,2-deleted'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_vgallery_videos`
--

CREATE TABLE `tb_vgallery_videos` (
  `id` int(11) NOT NULL,
  `vgallery_id` int(11) NOT NULL,
  `video_type` tinyint(4) NOT NULL COMMENT '0-Youtbe link, 1-Facebook embed code',
  `v_caption` text CHARACTER SET utf8 NOT NULL,
  `v_code` text NOT NULL,
  `v_description` text CHARACTER SET utf8,
  `image_name` text CHARACTER SET utf8 NOT NULL,
  `cover_display` enum('y','n') DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `filename` text CHARACTER SET utf8,
  `page_title` text CHARACTER SET utf8,
  `meta_keyword` text CHARACTER SET utf8,
  `meta_description` text CHARACTER SET utf8,
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_by_ip` text NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_on` datetime NOT NULL,
  `updated_by_ip` text NOT NULL,
  `deleted_by` int(11) NOT NULL,
  `deleted_on` datetime NOT NULL,
  `deleted_by_ip` text NOT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active,2-deleted'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_video`
--

CREATE TABLE `tb_video` (
  `id` int(11) NOT NULL,
  `title` text CHARACTER SET utf8,
  `trailor_video_embed_code` text,
  `video_source` enum('1','2') DEFAULT NULL COMMENT '1- youtube ,2-vimeo',
  `main_video_embed_code` text,
  `track_type_id` smallint(6) DEFAULT NULL,
  `custom_video_thumb` text,
  `duration` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL COMMENT 'id from tb_guru_basics',
  `category_id` int(11) DEFAULT NULL COMMENT 'id from tb_category',
  `level_id` int(11) DEFAULT NULL,
  `dp_level_name` text,
  `cost_type` enum('1','2','3') NOT NULL COMMENT '1- free,2- paid,3-Long term',
  `accessibility_type` enum('1','2','3') DEFAULT NULL COMMENT '1-independent ,2- part of a programme,3-both',
  `tags` text,
  `description` text,
  `includes` text,
  `what_you_learn` text,
  `requirements` text,
  `share_img` text,
  `initial_view_count` int(11) DEFAULT NULL,
  `actual_view_count` int(11) DEFAULT NULL,
  `average_rating` float DEFAULT NULL,
  `rate_1` int(11) NOT NULL,
  `rate_2` int(11) NOT NULL,
  `rate_3` int(11) NOT NULL,
  `rate_4` int(11) NOT NULL,
  `rate_5` int(11) NOT NULL,
  `int_rat_1` int(11) NOT NULL,
  `int_rat_2` int(11) NOT NULL,
  `int_rat_3` int(11) NOT NULL,
  `int_rat_4` int(11) NOT NULL,
  `int_rat_5` int(11) NOT NULL,
  `audio_file` text,
  `visible_platform` int(11) DEFAULT NULL COMMENT '1- desktop,2-mobile,3-both',
  `display_order` int(11) NOT NULL,
  `filename` text,
  `meta_title` text,
  `meta_keywords` text,
  `meta_description` text,
  `added_on` datetime DEFAULT NULL,
  `added_by` int(11) DEFAULT NULL,
  `added_ip` text,
  `last_updated_on` datetime DEFAULT NULL,
  `last_updated_by` int(11) DEFAULT NULL,
  `last_updated_by_ip` text,
  `deleted_on` datetime DEFAULT NULL,
  `deleted_by` int(11) DEFAULT NULL,
  `deleted_by_ip` text,
  `status` int(11) DEFAULT NULL COMMENT '0-private,1-public,2-deleted'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_video_track_type`
--

CREATE TABLE `tb_video_track_type` (
  `id` smallint(6) NOT NULL,
  `title` text NOT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_whatsnew_home`
--

CREATE TABLE `tb_whatsnew_home` (
  `id` int(11) NOT NULL,
  `type` int(11) NOT NULL COMMENT '1=Class,2=culture,3=Webinar,4=Product',
  `table_id` int(11) NOT NULL,
  `table_name` text NOT NULL,
  `webinar_dispaly_upto` datetime DEFAULT NULL,
  `status` int(11) NOT NULL COMMENT '0-inactive,1-active,2 -deleted',
  `added_by` int(11) NOT NULL,
  `added_on` datetime NOT NULL,
  `added_ip` text NOT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_ip` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student_login_attempt_failed`
--
ALTER TABLE `student_login_attempt_failed`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_admin`
--
ALTER TABLE `tb_admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_banner`
--
ALTER TABLE `tb_banner`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_cart`
--
ALTER TABLE `tb_cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_category`
--
ALTER TABLE `tb_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_category_cover_images`
--
ALTER TABLE `tb_category_cover_images`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_certificate_download`
--
ALTER TABLE `tb_certificate_download`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_class_music_payment`
--
ALTER TABLE `tb_class_music_payment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_collection`
--
ALTER TABLE `tb_collection`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_common_settings`
--
ALTER TABLE `tb_common_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_cost_package`
--
ALTER TABLE `tb_cost_package`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_countries`
--
ALTER TABLE `tb_countries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_coupon`
--
ALTER TABLE `tb_coupon`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_coupon_link`
--
ALTER TABLE `tb_coupon_link`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_coupon_student_link`
--
ALTER TABLE `tb_coupon_student_link`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_delivery_address`
--
ALTER TABLE `tb_delivery_address`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_delivery_details`
--
ALTER TABLE `tb_delivery_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_editor_images`
--
ALTER TABLE `tb_editor_images`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_faq`
--
ALTER TABLE `tb_faq`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_feedback`
--
ALTER TABLE `tb_feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_feedback_class`
--
ALTER TABLE `tb_feedback_class`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_feedback_interests`
--
ALTER TABLE `tb_feedback_interests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_feedback_topics`
--
ALTER TABLE `tb_feedback_topics`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_freeclass`
--
ALTER TABLE `tb_freeclass`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_freevideo`
--
ALTER TABLE `tb_freevideo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_guru_art_forms`
--
ALTER TABLE `tb_guru_art_forms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`,`category_id`,`status`),
  ADD KEY `guru_id_2` (`guru_id`,`category_id`);

--
-- Indexes for table `tb_guru_bank`
--
ALTER TABLE `tb_guru_bank`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_guru_basics`
--
ALTER TABLE `tb_guru_basics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`,`status`);

--
-- Indexes for table `tb_guru_description`
--
ALTER TABLE `tb_guru_description`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`,`guru_id`,`status`);

--
-- Indexes for table `tb_guru_social_links`
--
ALTER TABLE `tb_guru_social_links`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_language`
--
ALTER TABLE `tb_language`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_latest_updates`
--
ALTER TABLE `tb_latest_updates`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_level`
--
ALTER TABLE `tb_level`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_level_sub`
--
ALTER TABLE `tb_level_sub`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_marital_status`
--
ALTER TABLE `tb_marital_status`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_menu`
--
ALTER TABLE `tb_menu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `status` (`status`),
  ADD KEY `added_on` (`added_on`);

--
-- Indexes for table `tb_mobile_country_codes`
--
ALTER TABLE `tb_mobile_country_codes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music`
--
ALTER TABLE `tb_music`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_album`
--
ALTER TABLE `tb_music_album`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_album_artist`
--
ALTER TABLE `tb_music_album_artist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_album_category`
--
ALTER TABLE `tb_music_album_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_artist`
--
ALTER TABLE `tb_music_artist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_artist_category`
--
ALTER TABLE `tb_music_artist_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_category`
--
ALTER TABLE `tb_music_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_list`
--
ALTER TABLE `tb_music_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_package`
--
ALTER TABLE `tb_music_package`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_playlist_master`
--
ALTER TABLE `tb_music_playlist_master`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_music_track`
--
ALTER TABLE `tb_music_track`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_other_artist`
--
ALTER TABLE `tb_other_artist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_pages`
--
ALTER TABLE `tb_pages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_pgallery`
--
ALTER TABLE `tb_pgallery`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_picture`
--
ALTER TABLE `tb_picture`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_producer`
--
ALTER TABLE `tb_producer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product`
--
ALTER TABLE `tb_product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product_category`
--
ALTER TABLE `tb_product_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product_cost`
--
ALTER TABLE `tb_product_cost`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product_delivery`
--
ALTER TABLE `tb_product_delivery`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product_description`
--
ALTER TABLE `tb_product_description`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product_image`
--
ALTER TABLE `tb_product_image`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_product_video`
--
ALTER TABLE `tb_product_video`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_programme`
--
ALTER TABLE `tb_programme`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`,`category_id`);

--
-- Indexes for table `tb_programme_artist`
--
ALTER TABLE `tb_programme_artist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_programme_description`
--
ALTER TABLE `tb_programme_description`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`,`item_id`,`item_type`,`status`);

--
-- Indexes for table `tb_programme_video`
--
ALTER TABLE `tb_programme_video`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`,`programme_id`,`video_id`,`status`);

--
-- Indexes for table `tb_project`
--
ALTER TABLE `tb_project`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_purchase`
--
ALTER TABLE `tb_purchase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`,`transaction_status`),
  ADD KEY `transaction_status` (`transaction_status`,`added_on`),
  ADD KEY `payment_gateway` (`payment_gateway`,`transaction_status`,`added_on`);

--
-- Indexes for table `tb_purchase_items`
--
ALTER TABLE `tb_purchase_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`,`item_id`,`item_type`,`status`),
  ADD KEY `item_type` (`item_type`,`valid_from`,`status`),
  ADD KEY `purchase_id` (`purchase_id`,`item_type`,`valid_from`,`status`);

--
-- Indexes for table `tb_rating_review`
--
ALTER TABLE `tb_rating_review`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_revenue_deduction_heads`
--
ALTER TABLE `tb_revenue_deduction_heads`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_revenue_generate`
--
ALTER TABLE `tb_revenue_generate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_revenue_generate_sub`
--
ALTER TABLE `tb_revenue_generate_sub`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_revenue_settings_new`
--
ALTER TABLE `tb_revenue_settings_new`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_revenue_settings_new_head_split`
--
ALTER TABLE `tb_revenue_settings_new_head_split`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_shipping_details`
--
ALTER TABLE `tb_shipping_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_states`
--
ALTER TABLE `tb_states`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_student`
--
ALTER TABLE `tb_student`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_student_interested_categories`
--
ALTER TABLE `tb_student_interested_categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_student_login_log`
--
ALTER TABLE `tb_student_login_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `tb_student_topic_categories`
--
ALTER TABLE `tb_student_topic_categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_transaction_log`
--
ALTER TABLE `tb_transaction_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_vgallery`
--
ALTER TABLE `tb_vgallery`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_vgallery_videos`
--
ALTER TABLE `tb_vgallery_videos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_video`
--
ALTER TABLE `tb_video`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_video_track_type`
--
ALTER TABLE `tb_video_track_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_whatsnew_home`
--
ALTER TABLE `tb_whatsnew_home`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `student_login_attempt_failed`
--
ALTER TABLE `student_login_attempt_failed`
  MODIFY `id` bigint(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_admin`
--
ALTER TABLE `tb_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_banner`
--
ALTER TABLE `tb_banner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_cart`
--
ALTER TABLE `tb_cart`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_category`
--
ALTER TABLE `tb_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_category_cover_images`
--
ALTER TABLE `tb_category_cover_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_certificate_download`
--
ALTER TABLE `tb_certificate_download`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_class_music_payment`
--
ALTER TABLE `tb_class_music_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_collection`
--
ALTER TABLE `tb_collection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_common_settings`
--
ALTER TABLE `tb_common_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_cost_package`
--
ALTER TABLE `tb_cost_package`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_countries`
--
ALTER TABLE `tb_countries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_coupon`
--
ALTER TABLE `tb_coupon`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_coupon_link`
--
ALTER TABLE `tb_coupon_link`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_coupon_student_link`
--
ALTER TABLE `tb_coupon_student_link`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_delivery_address`
--
ALTER TABLE `tb_delivery_address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_delivery_details`
--
ALTER TABLE `tb_delivery_details`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_editor_images`
--
ALTER TABLE `tb_editor_images`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_faq`
--
ALTER TABLE `tb_faq`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_feedback`
--
ALTER TABLE `tb_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_feedback_class`
--
ALTER TABLE `tb_feedback_class`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_feedback_interests`
--
ALTER TABLE `tb_feedback_interests`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_feedback_topics`
--
ALTER TABLE `tb_feedback_topics`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_freeclass`
--
ALTER TABLE `tb_freeclass`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_freevideo`
--
ALTER TABLE `tb_freevideo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_guru_art_forms`
--
ALTER TABLE `tb_guru_art_forms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_guru_bank`
--
ALTER TABLE `tb_guru_bank`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_guru_basics`
--
ALTER TABLE `tb_guru_basics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_guru_description`
--
ALTER TABLE `tb_guru_description`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_guru_social_links`
--
ALTER TABLE `tb_guru_social_links`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_language`
--
ALTER TABLE `tb_language`
  MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_latest_updates`
--
ALTER TABLE `tb_latest_updates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_level`
--
ALTER TABLE `tb_level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_level_sub`
--
ALTER TABLE `tb_level_sub`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_marital_status`
--
ALTER TABLE `tb_marital_status`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_menu`
--
ALTER TABLE `tb_menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_mobile_country_codes`
--
ALTER TABLE `tb_mobile_country_codes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music`
--
ALTER TABLE `tb_music`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_album`
--
ALTER TABLE `tb_music_album`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_album_artist`
--
ALTER TABLE `tb_music_album_artist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_album_category`
--
ALTER TABLE `tb_music_album_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_artist`
--
ALTER TABLE `tb_music_artist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_artist_category`
--
ALTER TABLE `tb_music_artist_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_category`
--
ALTER TABLE `tb_music_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_list`
--
ALTER TABLE `tb_music_list`
  MODIFY `id` bigint(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_package`
--
ALTER TABLE `tb_music_package`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_playlist_master`
--
ALTER TABLE `tb_music_playlist_master`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_music_track`
--
ALTER TABLE `tb_music_track`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_other_artist`
--
ALTER TABLE `tb_other_artist`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_pages`
--
ALTER TABLE `tb_pages`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_pgallery`
--
ALTER TABLE `tb_pgallery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_picture`
--
ALTER TABLE `tb_picture`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_producer`
--
ALTER TABLE `tb_producer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product`
--
ALTER TABLE `tb_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product_category`
--
ALTER TABLE `tb_product_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product_cost`
--
ALTER TABLE `tb_product_cost`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product_delivery`
--
ALTER TABLE `tb_product_delivery`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product_description`
--
ALTER TABLE `tb_product_description`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product_image`
--
ALTER TABLE `tb_product_image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_product_video`
--
ALTER TABLE `tb_product_video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_programme`
--
ALTER TABLE `tb_programme`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_programme_artist`
--
ALTER TABLE `tb_programme_artist`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_programme_description`
--
ALTER TABLE `tb_programme_description`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_programme_video`
--
ALTER TABLE `tb_programme_video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_project`
--
ALTER TABLE `tb_project`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_purchase`
--
ALTER TABLE `tb_purchase`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_purchase_items`
--
ALTER TABLE `tb_purchase_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_rating_review`
--
ALTER TABLE `tb_rating_review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_revenue_deduction_heads`
--
ALTER TABLE `tb_revenue_deduction_heads`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_revenue_generate`
--
ALTER TABLE `tb_revenue_generate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_revenue_generate_sub`
--
ALTER TABLE `tb_revenue_generate_sub`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_revenue_settings_new`
--
ALTER TABLE `tb_revenue_settings_new`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_revenue_settings_new_head_split`
--
ALTER TABLE `tb_revenue_settings_new_head_split`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_shipping_details`
--
ALTER TABLE `tb_shipping_details`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_states`
--
ALTER TABLE `tb_states`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_student`
--
ALTER TABLE `tb_student`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_student_interested_categories`
--
ALTER TABLE `tb_student_interested_categories`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_student_login_log`
--
ALTER TABLE `tb_student_login_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_student_topic_categories`
--
ALTER TABLE `tb_student_topic_categories`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_transaction_log`
--
ALTER TABLE `tb_transaction_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_vgallery`
--
ALTER TABLE `tb_vgallery`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_vgallery_videos`
--
ALTER TABLE `tb_vgallery_videos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_video`
--
ALTER TABLE `tb_video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_video_track_type`
--
ALTER TABLE `tb_video_track_type`
  MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tb_whatsnew_home`
--
ALTER TABLE `tb_whatsnew_home`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
