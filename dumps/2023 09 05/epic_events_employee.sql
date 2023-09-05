-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: epic_events
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department_id` int NOT NULL,
  `encoded_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'albert','camus','gestion1',1,'$argon2id$v=19$m=65536,t=3,p=4$YnFFKptVhaYFqldkb7rETw$lFei5iQFlrNwFv11Jf/HSAXwZ16THNo5l2Q2JNcY/ck'),(2,'victor','hugo','commercial1',2,'$argon2id$v=19$m=65536,t=3,p=4$/kUTgWrAhFPVdC267akARQ$mwSpL0ue2y6A/83w7DCW4392Mb4wNdLo/3oewooObRA'),(3,'jean-baptiste','poquelin','support1',3,'$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),(4,'gestion','2','gestion2',1,'$argon2id$v=19$m=65536,t=3,p=4$px9xFTKHPsM8ADixnyxj5Q$+LVdw+MyrO38zUD1R8JXBPP43bEXMC9JcAiwoKo+s/4'),(5,'commercial','2','commercial2',2,'$argon2id$v=19$m=65536,t=3,p=4$iPISj3syltu40RCglB2P9Q$KHS9bgEnQ6CmkegpxUC3IlQZe5QyKcFUjpOkOH5uowQ'),(6,'support','2','support2',3,'$argon2id$v=19$m=65536,t=3,p=4$5rAXTR8P11nzJiV6KCsgYw$tdMBNLyeTiREQ1Vdxou3JLMejA0VJSgU/gCYD9GqLLk'),(9,'f','f','gf',2,'$argon2id$v=19$m=65536,t=3,p=4$svJvRCFRxSaBTOvMWCi5QA$2xVUXO3/8B7Dv7vv/RUneEKZjnLpVcpNMGF9g7iXrGE'),(10,'v','s','vs',1,'$argon2id$v=19$m=65536,t=3,p=4$3Z/lpZwcWdIJ96E97jjayw$YK6uS5U62/dtw+h63gsAYIHDx5C1HSHolGSzpWW86t0'),(11,'r','f','ef',1,'$argon2id$v=19$m=65536,t=3,p=4$yJ+92XB66l0ufEPv7WSVrQ$Y8ohmZnNrV2XGDnvCpF58D7lCuPfAu4cvnI/s9h3rVU'),(12,'qwe','rqwe','qew',1,'$argon2id$v=19$m=65536,t=3,p=4$ozhZoAkXFmPAwZkemQ3VjA$ni6BFzFFk4doRnx8xDonwv8CwIFtifc4Vp3iQkzJoD0'),(13,'df','df','df',1,'$argon2id$v=19$m=65536,t=3,p=4$XUveHHpM1iUmFd4uVe9LTA$WZgCgtXPCeD07vUlFxpdiveje1bqeBVvFfHdhjarrpE'),(14,'sdfg','sdfg','sf',1,'$argon2id$v=19$m=65536,t=3,p=4$GWNIJklUd0rWMnB7Lir/ng$HRf2S/b7W0K3jkVnBbjlEmLiCtzRPUB+nRsvjp4bVFw'),(15,'asfasdf','asdfasdf','asdfasdf',1,'$argon2id$v=19$m=65536,t=3,p=4$8vcndawmGK30vhccXPuYkg$pyIx1zi3QTkxKeHWAJyuGB615kyAnELGxX3yLlTucig'),(16,'asdf','asdf','asdf',1,'$argon2id$v=19$m=65536,t=3,p=4$8Dxm1HF9l6cNKL30nBOwGg$v1kn4kMaZcBzEA2/GcRyPSd9TSeI7MOcAilUCUt4kk4'),(17,'asdf','asd','fasdf',1,'$argon2id$v=19$m=65536,t=3,p=4$rqIdb8Iu6subInNS+2M9Ew$26z8I1Sx3VAmS+DUYeBRF+WaocKCgKSg7AsLIWGwudY'),(18,'asdf','asd','asd',1,'$argon2id$v=19$m=65536,t=3,p=4$na4PJOz/SsI9xTSxa7ggqA$O8Ta7ZnJQsDfu9ShHEFt2V6U/xkheJAaIHK6tY6F1ig'),(19,'asd','adsf','ads',1,'$argon2id$v=19$m=65536,t=3,p=4$tNdYVPpfIJoxCdpvbZxE7w$pLs2a05q+2xzHda9ncP2rGpLUFMkXi6K8BUdRUBqM/w'),(20,'asdf','adsf','asdf',1,'$argon2id$v=19$m=65536,t=3,p=4$+C2gjZCeuBtQuKYEpZo2bw$itiHq+x8K+Rb0uxHKDXcQnG550Ym9/zZyBDGnLilxOk'),(21,'asdf','asdf','asdf',1,'$argon2id$v=19$m=65536,t=3,p=4$wLX+nJshvZbFph7G/op+Hg$q18bcJrIwbbCCXb/iRghfMajE7D2fbEJcrDMEr0Oxqw'),(22,'Aasdf','asdf','asdf',1,'$argon2id$v=19$m=65536,t=3,p=4$ajg0wR8J7Q9vX+p/+7WY/Q$G5YMgIrym+0hwIIFCdMFPHJ5+OIvo0M9uOK2+BUKbHs'),(23,'asdf','Aasdf','asdf',1,'$argon2id$v=19$m=65536,t=3,p=4$9mrEEIHIyJ/dLdfKoMrLcw$Ek7Us0xWvcyHFT1ii+9+wupF7WdYSyOCgd6ZxYScir4'),(24,'asd','asdf','adf',1,'$argon2id$v=19$m=65536,t=3,p=4$UydPxwBhDuK3eGakLiVs8w$o6Z3pGEBr3GbbSW1xvUFNVMOoT4x5p0psteb+wmcQZo'),(25,'asdf','asdf','asdf',1,'$argon2id$v=19$m=65536,t=3,p=4$gENZuSG8E7faRmyacxwDWQ$4tuenE1OpkOw+8R9rXyKKVp1kRAemTjC/nCZYb4MGGs'),(26,'asdf','asdf','asdf',2,'$argon2id$v=19$m=65536,t=3,p=4$hefjc+FwYVv6XdRvJkjIFQ$2cY8fza6mkgJuutarkXamKm79gHmeoFTIoSbGj90JCc');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-05 17:13:16
