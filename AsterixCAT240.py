import binascii, struct, socket, threading, time

azimuthCount = 0
videoRecordHeader = 0

class AsterixCAT240:
    def __init__(self):
        self.MCAST_GRP = "239.0.0.1"
        self.MCAST_PORT = 4433

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


    def CAT(self, PACKET):
        if PACKET != '':
            category = PACKET[0:2]
            return int(category, 16)

    def LENGHT(self, PACKET):
        if PACKET != '':
            packetLenght = PACKET[2:6]
            return int(packetLenght, 16)

    def FSPEC(self, PACKET):
        if PACKET != '':
            fspec = PACKET[6:10]
            return int(fspec, 16)

    def DSI(self, PACKET):
        if PACKET != '':
            dataSourceIdentifier = PACKET[10:14]
            return dataSourceIdentifier

    def MSGTYPE(self, PACKET):
        if PACKET != '':
            messageType = PACKET[14:16]
            return messageType

    def VRH(self, PACKET):
        if PACKET != '':
            videoRecordHeader = PACKET[16:24]
            return int(videoRecordHeader, 16)

    def START_AZ(self, PACKET):
        if PACKET != '':
            azimuth = 0
            # bearing = self.PACKET[24:28]
            bearing = PACKET
            bearing_byte = int(bearing, 16)
            bearing_bin = format(bearing_byte, '16b')
            for azimuths in range(len(bearing_bin)):
                if bearing_bin[azimuths] == '1':
                    azimuth = 360 / pow(2, azimuths + 1) + azimuth
            return azimuth

    def START_RG(self, PACKET):
        if PACKET != '':
            startRange = PACKET[32:40]
            return startRange

    def CELL_DUR(self, PACKET):
        if PACKET != '':
            cellDuration = PACKET[40:48]
            return cellDuration

    def COMP_FLAG(self, PACKET):
        if PACKET != '':
            compression = PACKET[48:50]
            # COMPRESSION = COMPRESSION[7]
            return compression

    def RES(self, PACKET):
        if PACKET != '':
            resolution = PACKET[50:52]
            return resolution

    def NB_VB(self, PACKET):
        if PACKET != '':
            videoOctet = PACKET[52:56]
            return videoOctet

    def NB_CELLS(self, PACKET):
        if PACKET != '':
            cellsazimuthCounts = PACKET[56:62]
            return cellsazimuthCounts

    def VIDEO_azimuthCount(self, PACKET):
        if PACKET != '':
            videoBlockCounter = PACKET[62:64]
            return videoBlockCounter

    def VIDEO_BLOCK(self, PACKET):
        if PACKET != '':
            video = PACKET[64:len(PACKET) * 2]
            return video


    def SEND(self, PACKET=b'', MCAST_GRP="239.0.0.1", MCAST_PORT=4433):
        self.MCAST_GRP = MCAST_GRP
        self.MCAST_PORT = MCAST_PORT

        self.sock.sendto(PACKET, (MCAST_GRP, MCAST_PORT))

    def REC(self, MCAST_PORT=4433,  LEN=1056):
        self.MCAST_PORT = MCAST_PORT
        self.LEN = LEN

        PACKET, addr = self.sock.recvfrom(LEN)
        PACKET = binascii.hexlify(PACKET)
        return PACKET

    def canvasGenerator(self, MCAST_GRP="239.0.0.1", MCAST_PORT=4433, PATTERN=1):
        global azimuthCount, videoRecordHeader

        # azimuthCount = 0
        # videoRecordHeader = 0

        self.MCAST_GRP = MCAST_GRP
        self.MCAST_PORT = MCAST_PORT

        if PATTERN == 1:
            message = b'f00420e7a07de9020001554bb318b31800000000' + b'01312d00' + b'0004' + b'0400' + b'000400' + b'10' + b'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff101010101010101010101010101010101010101010101010101010101010101020202020202020202020202020202020202020202020202020202020202020203030303030303030303030303030303030303030303030303030303030303030404040404040404040404040404040404040404040404040404040404040404050505050505050505050505050505050505050505050505050505050505050506060606060606060606060606060606060606060606060606060606060606060707070707070707070707070707070707070707070707070707070707070707080808080808080808080808080808080808080808080808080808080808080809090909090909090909090909090909090909090909090909090909090909090a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f10101010101010101010101010101010101010101010101010101010101010101111111111111111111111111111111111111111111111111111111111111111121212121212121212121212121212121212121212121212121212121212121213131313131313131313131313131313131313131313131313131313131313131414141414141414141414141414141414141414141414141414141414141414151515151515151515151515151515151515151515151515151515151515151516161616161616161616161616161616161616161616161616161616161616161717171717171717171717171717171717171717171717171717171717171717181818181818181818181818181818181818181818181818181818181818181819191919191919191919191919191919191919191919191919191919191919191a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1d1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f'

        elif PATTERN == 2:
            message = b'f00420e7a07de90200e8fcf31210121000000000' + b'01312d00' + b'0004' + b'0400' + b'000400' + b'10' + ('66' * 1024).encode()
            
        elif PATTERN == 3:
            message = b'f00420e7a07de9020001554bb318b31800000000' + b'07c9d0a0' + b'0004' + b'0400' + b'000400' + b'10' + ('33' * 1024).encode()

        if azimuthCount == 2000:
            azimuthCount = 0
        if videoRecordHeader == 4294967295:
            videoRecordHeader = 0

        azimuths = [b'0008', b'0028', b'0048', b'0068', b'0088', b'00a8', b'00c8', b'00e8', b'0110', b'0130', b'0150',
                    b'0170', b'0190', b'01b0', b'01d0', b'01f0', b'0210', b'0230', b'0258', b'0278', b'0298', b'02b8',
                    b'02d8', b'02f8', b'0318', b'0338', b'0358', b'0378', b'03a0', b'03c0', b'03e0', b'0400', b'0420',
                    b'0440', b'0460', b'0480', b'04a0', b'04c0', b'04e0', b'0508', b'0528', b'0548', b'0568', b'0588',
                    b'05a8', b'05c8', b'05e8', b'0608', b'0628', b'0648', b'0670', b'0690', b'06b0', b'06d0', b'06f0',
                    b'0710', b'0730', b'0750', b'0770', b'0790', b'07b0', b'07d8', b'07f8', b'0818', b'0838', b'0858',
                    b'0878', b'0898', b'08b8', b'08d8', b'08f8', b'0920', b'0940', b'0960', b'0980', b'09a0', b'09c0',
                    b'09e0', b'0a00', b'0a20', b'0a40', b'0a68', b'0a88', b'0aa8', b'0ac8', b'0ae8', b'0b08', b'0b28',
                    b'0b48', b'0b68', b'0b88', b'0bb0', b'0bd0', b'0bf0', b'0c10', b'0c30', b'0c50', b'0c70', b'0c90',
                    b'0cb0', b'0cd0', b'0cf8', b'0d18', b'0d38', b'0d58', b'0d78', b'0d98', b'0db8', b'0dd8', b'0df8',
                    b'0e18', b'0e40', b'0e60', b'0e80', b'0ea0', b'0ec0', b'0ee0', b'0f00', b'0f20', b'0f40', b'0f60',
                    b'0f80', b'0fa8', b'0fc8', b'0fe8', b'1008', b'1028', b'1048', b'1068', b'1088', b'10a8', b'10c8',
                    b'10e8', b'1110', b'1130', b'1150', b'1170', b'1190', b'11b0', b'11d0', b'11f0', b'1210', b'1230',
                    b'1250', b'1278', b'1298', b'12b8', b'12d8', b'12f8', b'1318', b'1338', b'1358', b'1378', b'1398',
                    b'13c0', b'13e0', b'1400', b'1420', b'1440', b'1460', b'1480', b'14a0', b'14c0', b'14e0', b'1508',
                    b'1528', b'1548', b'1568', b'1588', b'15a8', b'15c8', b'15e8', b'1608', b'1628', b'1650', b'1670',
                    b'1690', b'16b0', b'16d0', b'16f0', b'1710', b'1730', b'1750', b'1770', b'1798', b'17b8', b'17d8',
                    b'17f8', b'1818', b'1838', b'1858', b'1878', b'1898', b'18b8', b'18e0', b'1900', b'1920', b'1940',
                    b'1960', b'1980', b'19a0', b'19c0', b'19e0', b'1a00', b'1a20', b'1a48', b'1a68', b'1a88', b'1aa8',
                    b'1ac8', b'1ae8', b'1b08', b'1b28', b'1b48', b'1b68', b'1b88', b'1bb0', b'1bd0', b'1bf0', b'1c10',
                    b'1c30', b'1c50', b'1c70', b'1c90', b'1cb0', b'1cd0', b'1cf0', b'1d18', b'1d38', b'1d58', b'1d78',
                    b'1d98', b'1db8', b'1dd8', b'1df8', b'1e18', b'1e38', b'1e60', b'1e80', b'1ea0', b'1ec0', b'1ee0',
                    b'1f00', b'1f20', b'1f40', b'1f60', b'1f80', b'1fa0', b'1fc8', b'1fe8', b'2008', b'2028', b'2048',
                    b'2068', b'2088', b'20a8', b'20c8', b'20e8', b'2108', b'2130', b'2150', b'2170', b'2190', b'21b0',
                    b'21d0', b'21f0', b'2210', b'2230', b'2250', b'2270', b'2298', b'22b8', b'22d8', b'22f8', b'2318',
                    b'2338', b'2358', b'2378', b'2398', b'23b8', b'23d8', b'2400', b'2420', b'2440', b'2460', b'2480',
                    b'24a0', b'24c0', b'24e0', b'2500', b'2520', b'2548', b'2568', b'2588', b'25a8', b'25c8', b'25e8',
                    b'2608', b'2628', b'2648', b'2668', b'2690', b'26b0', b'26d0', b'26f0', b'2710', b'2730', b'2750',
                    b'2770', b'2790', b'27b0', b'27d8', b'27f8', b'2818', b'2838', b'2858', b'2878', b'2898', b'28b8',
                    b'28d8', b'28f8', b'2920', b'2940', b'2960', b'2980', b'29a0', b'29c0', b'29e0', b'2a00', b'2a20',
                    b'2a40', b'2a68', b'2a88', b'2aa8', b'2ac8', b'2ae8', b'2b08', b'2b28', b'2b48', b'2b68', b'2b88',
                    b'2ba8', b'2bd0', b'2bf0', b'2c10', b'2c30', b'2c50', b'2c70', b'2c90', b'2cb0', b'2cd0', b'2cf0',
                    b'2d10', b'2d38', b'2d58', b'2d78', b'2d98', b'2db8', b'2dd8', b'2df8', b'2e18', b'2e38', b'2e58',
                    b'2e80', b'2ea0', b'2ec0', b'2ee0', b'2f00', b'2f20', b'2f40', b'2f60', b'2f80', b'2fa0', b'2fc0',
                    b'2fe8', b'3008', b'3028', b'3048', b'3068', b'3088', b'30a8', b'30c8', b'30e8', b'3108', b'3130',
                    b'3150', b'3170', b'3190', b'31b0', b'31d0', b'31f0', b'3210', b'3230', b'3250', b'3278', b'3298',
                    b'32b8', b'32d8', b'32f8', b'3318', b'3338', b'3358', b'3378', b'3398', b'33c0', b'33e0', b'3400',
                    b'3420', b'3440', b'3460', b'3480', b'34a0', b'34c0', b'34e0', b'3508', b'3528', b'3548', b'3568',
                    b'3588', b'35a8', b'35c8', b'35e8', b'3608', b'3628', b'3648', b'3670', b'3690', b'36b0', b'36d0',
                    b'36f0', b'3710', b'3730', b'3750', b'3770', b'3790', b'37b0', b'37d8', b'37f8', b'3818', b'3838',
                    b'3858', b'3878', b'3898', b'38b8', b'38d8', b'38f8', b'3920', b'3940', b'3960', b'3980', b'39a0',
                    b'39c0', b'39e0', b'3a00', b'3a20', b'3a40', b'3a60', b'3a88', b'3aa8', b'3ac8', b'3ae8', b'3b08',
                    b'3b28', b'3b48', b'3b68', b'3b88', b'3ba8', b'3bd0', b'3bf0', b'3c10', b'3c30', b'3c50', b'3c70',
                    b'3c90', b'3cb0', b'3cd0', b'3cf0', b'3d18', b'3d38', b'3d58', b'3d78', b'3d98', b'3db8', b'3dd8',
                    b'3df8', b'3e18', b'3e38', b'3e60', b'3e80', b'3ea0', b'3ec0', b'3ee0', b'3f00', b'3f20', b'3f40',
                    b'3f60', b'3f80', b'3fa8', b'3fc8', b'3fe8', b'4008', b'4028', b'4048', b'4068', b'4088', b'40a8',
                    b'40c8', b'40e8', b'4110', b'4130', b'4150', b'4170', b'4190', b'41b0', b'41d0', b'41f0', b'4210',
                    b'4230', b'4258', b'4278', b'4298', b'42b8', b'42d8', b'42f8', b'4318', b'4338', b'4358', b'4378',
                    b'4398', b'43c0', b'43e0', b'4400', b'4420', b'4440', b'4460', b'4480', b'44a0', b'44c0', b'44e0',
                    b'4500', b'4528', b'4548', b'4568', b'4588', b'45a8', b'45c8', b'45e8', b'4608', b'4628', b'4648',
                    b'4668', b'4690', b'46b0', b'46d0', b'46f0', b'4710', b'4730', b'4750', b'4770', b'4790', b'47b0',
                    b'47d8', b'47f8', b'4818', b'4838', b'4858', b'4878', b'4898', b'48b8', b'48d8', b'48f8', b'4920',
                    b'4940', b'4960', b'4980', b'49a0', b'49c0', b'49e0', b'4a00', b'4a20', b'4a40', b'4a68', b'4a88',
                    b'4aa8', b'4ac8', b'4ae8', b'4b08', b'4b28', b'4b48', b'4b68', b'4b88', b'4bb0', b'4bd0', b'4bf0',
                    b'4c10', b'4c30', b'4c50', b'4c70', b'4c90', b'4cb0', b'4cd0', b'4cf8', b'4d18', b'4d38', b'4d58',
                    b'4d78', b'4d98', b'4db8', b'4dd8', b'4df8', b'4e18', b'4e38', b'4e60', b'4e80', b'4ea0', b'4ec0',
                    b'4ee0', b'4f00', b'4f20', b'4f40', b'4f60', b'4f80', b'4fa0', b'4fc8', b'4fe8', b'5008', b'5028',
                    b'5048', b'5068', b'5088', b'50a8', b'50c8', b'50e8', b'5108', b'5130', b'5150', b'5170', b'5190',
                    b'51b0', b'51d0', b'51f0', b'5210', b'5230', b'5250', b'5278', b'5298', b'52b8', b'52d8', b'52f8',
                    b'5318', b'5338', b'5358', b'5378', b'5398', b'53c0', b'53e0', b'5400', b'5420', b'5440', b'5460',
                    b'5480', b'54a0', b'54c0', b'54e0', b'5508', b'5528', b'5548', b'5568', b'5588', b'55a8', b'55c8',
                    b'55e8', b'5608', b'5628', b'5650', b'5670', b'5690', b'56b0', b'56d0', b'56f0', b'5710', b'5730',
                    b'5750', b'5770', b'5798', b'57b8', b'57d8', b'57f8', b'5818', b'5838', b'5858', b'5878', b'5898',
                    b'58b8', b'58d8', b'5900', b'5920', b'5940', b'5960', b'5980', b'59a0', b'59c0', b'59e0', b'5a00',
                    b'5a20', b'5a40', b'5a68', b'5a88', b'5aa8', b'5ac8', b'5ae8', b'5b08', b'5b28', b'5b48', b'5b68',
                    b'5b88', b'5ba8', b'5bd0', b'5bf0', b'5c10', b'5c30', b'5c50', b'5c70', b'5c90', b'5cb0', b'5cd0',
                    b'5cf0', b'5d18', b'5d38', b'5d58', b'5d78', b'5d98', b'5db8', b'5dd8', b'5df8', b'5e18', b'5e38',
                    b'5e58', b'5e80', b'5ea0', b'5ec0', b'5ee0', b'5f00', b'5f20', b'5f40', b'5f60', b'5f80', b'5fa0',
                    b'5fc0', b'5fe8', b'6008', b'6028', b'6048', b'6068', b'6088', b'60a8', b'60c8', b'60e8', b'6108',
                    b'6128', b'6150', b'6170', b'6190', b'61b0', b'61d0', b'61f0', b'6210', b'6230', b'6250', b'6270',
                    b'6298', b'62b8', b'62d8', b'62f8', b'6318', b'6338', b'6358', b'6378', b'6398', b'63b8', b'63e0',
                    b'6400', b'6420', b'6440', b'6460', b'6480', b'64a0', b'64c0', b'64e0', b'6500', b'6528', b'6548',
                    b'6568', b'6588', b'65a8', b'65c8', b'65e8', b'6608', b'6628', b'6648', b'6670', b'6690', b'66b0',
                    b'66d0', b'66f0', b'6710', b'6730', b'6750', b'6770', b'6790', b'67b8', b'67d8', b'67f8', b'6818',
                    b'6838', b'6858', b'6878', b'6898', b'68b8', b'68d8', b'68f8', b'6920', b'6940', b'6960', b'6980',
                    b'69a0', b'69c0', b'69e0', b'6a00', b'6a20', b'6a40', b'6a60', b'6a88', b'6aa8', b'6ac8', b'6ae8',
                    b'6b08', b'6b28', b'6b48', b'6b68', b'6b88', b'6ba8', b'6bc8', b'6bf0', b'6c10', b'6c30', b'6c50',
                    b'6c70', b'6c90', b'6cb0', b'6cd0', b'6cf0', b'6d10', b'6d38', b'6d58', b'6d78', b'6d98', b'6db8',
                    b'6dd8', b'6df8', b'6e18', b'6e38', b'6e58', b'6e78', b'6ea0', b'6ec0', b'6ee0', b'6f00', b'6f20',
                    b'6f40', b'6f60', b'6f80', b'6fa0', b'6fc0', b'6fe8', b'7008', b'7028', b'7048', b'7068', b'7088',
                    b'70a8', b'70c8', b'70e8', b'7108', b'7130', b'7150', b'7170', b'7190', b'71b0', b'71d0', b'71f0',
                    b'7210', b'7230', b'7250', b'7278', b'7298', b'72b8', b'72d8', b'72f8', b'7318', b'7338', b'7358',
                    b'7378', b'7398', b'73c0', b'73e0', b'7400', b'7420', b'7440', b'7460', b'7480', b'74a0', b'74c0',
                    b'74e0', b'7500', b'7528', b'7548', b'7568', b'7588', b'75a8', b'75c8', b'75e8', b'7608', b'7628',
                    b'7648', b'7668', b'7690', b'76b0', b'76d0', b'76f0', b'7710', b'7730', b'7750', b'7770', b'7790',
                    b'77b0', b'77d8', b'77f8', b'7818', b'7838', b'7858', b'7878', b'7898', b'78b8', b'78d8', b'78f8',
                    b'7918', b'7940', b'7960', b'7980', b'79a0', b'79c0', b'79e0', b'7a00', b'7a20', b'7a40', b'7a60',
                    b'7a88', b'7aa8', b'7ac8', b'7ae8', b'7b08', b'7b28', b'7b48', b'7b68', b'7b88', b'7ba8', b'7bd0',
                    b'7bf0', b'7c10', b'7c30', b'7c50', b'7c70', b'7c90', b'7cb0', b'7cd0', b'7cf0', b'7d18', b'7d38',
                    b'7d58', b'7d78', b'7d98', b'7db8', b'7dd8', b'7df8', b'7e18', b'7e38', b'7e60', b'7e80', b'7ea0',
                    b'7ec0', b'7ee0', b'7f00', b'7f20', b'7f40', b'7f60', b'7f80', b'7fa0', b'7fc8', b'7fe8', b'8008',
                    b'8028', b'8048', b'8068', b'8088', b'80a8', b'80c8', b'80e8', b'8110', b'8130', b'8150', b'8170',
                    b'8190', b'81b0', b'81d0', b'81f0', b'8210', b'8230', b'8250', b'8278', b'8298', b'82b8', b'82d8',
                    b'82f8', b'8318', b'8338', b'8358', b'8378', b'8398', b'83b8', b'83e0', b'8400', b'8420', b'8440',
                    b'8460', b'8480', b'84a0', b'84c0', b'84e0', b'8500', b'8528', b'8548', b'8568', b'8588', b'85a8',
                    b'85c8', b'85e8', b'8608', b'8628', b'8648', b'8670', b'8690', b'86b0', b'86d0', b'86f0', b'8710',
                    b'8730', b'8750', b'8770', b'8790', b'87b8', b'87d8', b'87f8', b'8818', b'8838', b'8858', b'8878',
                    b'8898', b'88b8', b'88d8', b'8900', b'8920', b'8940', b'8960', b'8980', b'89a0', b'89c0', b'89e0',
                    b'8a00', b'8a20', b'8a48', b'8a68', b'8a88', b'8aa8', b'8ac8', b'8ae8', b'8b08', b'8b28', b'8b48',
                    b'8b68', b'8b88', b'8bb0', b'8bd0', b'8bf0', b'8c10', b'8c30', b'8c50', b'8c70', b'8c90', b'8cb0',
                    b'8cd0', b'8cf0', b'8d18', b'8d38', b'8d58', b'8d78', b'8d98', b'8db8', b'8dd8', b'8df8', b'8e18',
                    b'8e38', b'8e58', b'8e80', b'8ea0', b'8ec0', b'8ee0', b'8f00', b'8f20', b'8f40', b'8f60', b'8f80',
                    b'8fa0', b'8fc8', b'8fe8', b'9008', b'9028', b'9048', b'9068', b'9088', b'90a8', b'90c8', b'90e8',
                    b'9110', b'9130', b'9150', b'9170', b'9190', b'91b0', b'91d0', b'91f0', b'9210', b'9230', b'9258',
                    b'9278', b'9298', b'92b8', b'92d8', b'92f8', b'9318', b'9338', b'9358', b'9378', b'93a0', b'93c0',
                    b'93e0', b'9400', b'9420', b'9440', b'9460', b'9480', b'94a0', b'94c0', b'94e8', b'9508', b'9528',
                    b'9548', b'9568', b'9588', b'95a8', b'95c8', b'95e8', b'9608', b'9628', b'9650', b'9670', b'9690',
                    b'96b0', b'96d0', b'96f0', b'9710', b'9730', b'9750', b'9770', b'9790', b'97b8', b'97d8', b'97f8',
                    b'9818', b'9838', b'9858', b'9878', b'9898', b'98b8', b'98d8', b'98f8', b'9920', b'9940', b'9960',
                    b'9980', b'99a0', b'99c0', b'99e0', b'9a00', b'9a20', b'9a40', b'9a60', b'9a88', b'9aa8', b'9ac8',
                    b'9ae8', b'9b08', b'9b28', b'9b48', b'9b68', b'9b88', b'9ba8', b'9bd0', b'9bf0', b'9c10', b'9c30',
                    b'9c50', b'9c70', b'9c90', b'9cb0', b'9cd0', b'9cf0', b'9d10', b'9d38', b'9d58', b'9d78', b'9d98',
                    b'9db8', b'9dd8', b'9df8', b'9e18', b'9e38', b'9e58', b'9e78', b'9ea0', b'9ec0', b'9ee0', b'9f00',
                    b'9f20', b'9f40', b'9f60', b'9f80', b'9fa0', b'9fc0', b'9fe0', b'a008', b'a028', b'a048', b'a068',
                    b'a088', b'a0a8', b'a0c8', b'a0e8', b'a108', b'a128', b'a150', b'a170', b'a190', b'a1b0', b'a1d0',
                    b'a1f0', b'a210', b'a230', b'a250', b'a270', b'a298', b'a2b8', b'a2d8', b'a2f8', b'a318', b'a338',
                    b'a358', b'a378', b'a398', b'a3b8', b'a3e0', b'a400', b'a420', b'a440', b'a460', b'a480', b'a4a0',
                    b'a4c0', b'a4e0', b'a500', b'a528', b'a548', b'a568', b'a588', b'a5a8', b'a5c8', b'a5e8', b'a608',
                    b'a628', b'a648', b'a670', b'a690', b'a6b0', b'a6d0', b'a6f0', b'a710', b'a730', b'a750', b'a770',
                    b'a790', b'a7b0', b'a7d8', b'a7f8', b'a818', b'a838', b'a858', b'a878', b'a898', b'a8b8', b'a8d8',
                    b'a8f8', b'a918', b'a940', b'a960', b'a980', b'a9a0', b'a9c0', b'a9e0', b'aa00', b'aa20', b'aa40',
                    b'aa60', b'aa80', b'aaa8', b'aac8', b'aae8', b'ab08', b'ab28', b'ab48', b'ab68', b'ab88', b'aba8',
                    b'abc8', b'abf0', b'ac10', b'ac30', b'ac50', b'ac70', b'ac90', b'acb0', b'acd0', b'acf0', b'ad10',
                    b'ad38', b'ad58', b'ad78', b'ad98', b'adb8', b'add8', b'adf8', b'ae18', b'ae38', b'ae58', b'ae80',
                    b'aea0', b'aec0', b'aee0', b'af00', b'af20', b'af40', b'af60', b'af80', b'afa0', b'afc8', b'afe8',
                    b'b008', b'b028', b'b048', b'b068', b'b088', b'b0a8', b'b0c8', b'b0e8', b'b110', b'b130', b'b150',
                    b'b170', b'b190', b'b1b0', b'b1d0', b'b1f0', b'b210', b'b230', b'b250', b'b278', b'b298', b'b2b8',
                    b'b2d8', b'b2f8', b'b318', b'b338', b'b358', b'b378', b'b398', b'b3b8', b'b3e0', b'b400', b'b420',
                    b'b440', b'b460', b'b480', b'b4a0', b'b4c0', b'b4e0', b'b500', b'b520', b'b548', b'b568', b'b588',
                    b'b5a8', b'b5c8', b'b5e8', b'b608', b'b628', b'b648', b'b668', b'b690', b'b6b0', b'b6d0', b'b6f0',
                    b'b710', b'b730', b'b750', b'b770', b'b790', b'b7b0', b'b7d8', b'b7f8', b'b818', b'b838', b'b858',
                    b'b878', b'b898', b'b8b8', b'b8d8', b'b8f8', b'b920', b'b940', b'b960', b'b980', b'b9a0', b'b9c0',
                    b'b9e0', b'ba00', b'ba20', b'ba40', b'ba68', b'ba88', b'baa8', b'bac8', b'bae8', b'bb08', b'bb28',
                    b'bb48', b'bb68', b'bb88', b'bbb0', b'bbd0', b'bbf0', b'bc10', b'bc30', b'bc50', b'bc70', b'bc90',
                    b'bcb0', b'bcd0', b'bcf0', b'bd18', b'bd38', b'bd58', b'bd78', b'bd98', b'bdb8', b'bdd8', b'bdf8',
                    b'be18', b'be38', b'be58', b'be80', b'bea0', b'bec0', b'bee0', b'bf00', b'bf20', b'bf40', b'bf60',
                    b'bf80', b'bfa0', b'bfc8', b'bfe8', b'c008', b'c028', b'c048', b'c068', b'c088', b'c0a8', b'c0c8',
                    b'c0e8', b'c108', b'c130', b'c150', b'c170', b'c190', b'c1b0', b'c1d0', b'c1f0', b'c210', b'c230',
                    b'c250', b'c270', b'c298', b'c2b8', b'c2d8', b'c2f8', b'c318', b'c338', b'c358', b'c378', b'c398',
                    b'c3b8', b'c3e0', b'c400', b'c420', b'c440', b'c460', b'c480', b'c4a0', b'c4c0', b'c4e0', b'c500',
                    b'c528', b'c548', b'c568', b'c588', b'c5a8', b'c5c8', b'c5e8', b'c608', b'c628', b'c648', b'c670',
                    b'c690', b'c6b0', b'c6d0', b'c6f0', b'c710', b'c730', b'c750', b'c770', b'c790', b'c7b8', b'c7d8',
                    b'c7f8', b'c818', b'c838', b'c858', b'c878', b'c898', b'c8b8', b'c8d8', b'c900', b'c920', b'c940',
                    b'c960', b'c980', b'c9a0', b'c9c0', b'c9e0', b'ca00', b'ca20', b'ca40', b'ca68', b'ca88', b'caa8',
                    b'cac8', b'cae8', b'cb08', b'cb28', b'cb48', b'cb68', b'cb88', b'cba8', b'cbd0', b'cbf0', b'cc10',
                    b'cc30', b'cc50', b'cc70', b'cc90', b'ccb0', b'ccd0', b'ccf0', b'cd10', b'cd38', b'cd58', b'cd78',
                    b'cd98', b'cdb8', b'cdd8', b'cdf8', b'ce18', b'ce38', b'ce58', b'ce80', b'cea0', b'cec0', b'cee0',
                    b'cf00', b'cf20', b'cf40', b'cf60', b'cf80', b'cfa0', b'cfc8', b'cfe8', b'd008', b'd028', b'd048',
                    b'd068', b'd088', b'd0a8', b'd0c8', b'd0e8', b'd110', b'd130', b'd150', b'd170', b'd190', b'd1b0',
                    b'd1d0', b'd1f0', b'd210', b'd230', b'd258', b'd278', b'd298', b'd2b8', b'd2d8', b'd2f8', b'd318',
                    b'd338', b'd358', b'd378', b'd3a0', b'd3c0', b'd3e0', b'd400', b'd420', b'd440', b'd460', b'd480',
                    b'd4a0', b'd4c0', b'd4e0', b'd508', b'd528', b'd548', b'd568', b'd588', b'd5a8', b'd5c8', b'd5e8',
                    b'd608', b'd628', b'd648', b'd670', b'd690', b'd6b0', b'd6d0', b'd6f0', b'd710', b'd730', b'd750',
                    b'd770', b'd790', b'd7b0', b'd7d8', b'd7f8', b'd818', b'd838', b'd858', b'd878', b'd898', b'd8b8',
                    b'd8d8', b'd8f8', b'd918', b'd940', b'd960', b'd980', b'd9a0', b'd9c0', b'd9e0', b'da00', b'da20',
                    b'da40', b'da60', b'da88', b'daa8', b'dac8', b'dae8', b'db08', b'db28', b'db48', b'db68', b'db88',
                    b'dba8', b'dbc8', b'dbf0', b'dc10', b'dc30', b'dc50', b'dc70', b'dc90', b'dcb0', b'dcd0', b'dcf0',
                    b'dd10', b'dd30', b'dd58', b'dd78', b'dd98', b'ddb8', b'ddd8', b'ddf8', b'de18', b'de38', b'de58',
                    b'de78', b'dea0', b'dec0', b'dee0', b'df00', b'df20', b'df40', b'df60', b'df80', b'dfa0', b'dfc0',
                    b'dfe8', b'e008', b'e028', b'e048', b'e068', b'e088', b'e0a8', b'e0c8', b'e0e8', b'e108', b'e130',
                    b'e150', b'e170', b'e190', b'e1b0', b'e1d0', b'e1f0', b'e210', b'e230', b'e250', b'e278', b'e298',
                    b'e2b8', b'e2d8', b'e2f8', b'e318', b'e338', b'e358', b'e378', b'e398', b'e3c0', b'e3e0', b'e400',
                    b'e420', b'e440', b'e460', b'e480', b'e4a0', b'e4c0', b'e4e0', b'e500', b'e528', b'e548', b'e568',
                    b'e588', b'e5a8', b'e5c8', b'e5e8', b'e608', b'e628', b'e648', b'e668', b'e690', b'e6b0', b'e6d0',
                    b'e6f0', b'e710', b'e730', b'e750', b'e770', b'e790', b'e7b0', b'e7d0', b'e7f8', b'e818', b'e838',
                    b'e858', b'e878', b'e898', b'e8b8', b'e8d8', b'e8f8', b'e918', b'e938', b'e960', b'e980', b'e9a0',
                    b'e9c0', b'e9e0', b'ea00', b'ea20', b'ea40', b'ea60', b'ea80', b'eaa8', b'eac8', b'eae8', b'eb08',
                    b'eb28', b'eb48', b'eb68', b'eb88', b'eba8', b'ebc8', b'ebf0', b'ec10', b'ec30', b'ec50', b'ec70',
                    b'ec90', b'ecb0', b'ecd0', b'ecf0', b'ed10', b'ed38', b'ed58', b'ed78', b'ed98', b'edb8', b'edd8',
                    b'edf8', b'ee18', b'ee38', b'ee58', b'ee80', b'eea0', b'eec0', b'eee0', b'ef00', b'ef20', b'ef40',
                    b'ef60', b'ef80', b'efa0', b'efc8', b'efe8', b'f008', b'f028', b'f048', b'f068', b'f088', b'f0a8',
                    b'f0c8', b'f0e8', b'f108', b'f130', b'f150', b'f170', b'f190', b'f1b0', b'f1d0', b'f1f0', b'f210',
                    b'f230', b'f250', b'f270', b'f298', b'f2b8', b'f2d8', b'f2f8', b'f318', b'f338', b'f358', b'f378',
                    b'f398', b'f3b8', b'f3d8', b'f400', b'f420', b'f440', b'f460', b'f480', b'f4a0', b'f4c0', b'f4e0',
                    b'f500', b'f520', b'f548', b'f568', b'f588', b'f5a8', b'f5c8', b'f5e8', b'f608', b'f628', b'f648',
                    b'f668', b'f690', b'f6b0', b'f6d0', b'f6f0', b'f710', b'f730', b'f750', b'f770', b'f790', b'f7b0',
                    b'f7d8', b'f7f8', b'f818', b'f838', b'f858', b'f878', b'f898', b'f8b8', b'f8d8', b'f8f8', b'f920',
                    b'f940', b'f960', b'f980', b'f9a0', b'f9c0', b'f9e0', b'fa00', b'fa20', b'fa40', b'fa68', b'fa88',
                    b'faa8', b'fac8', b'fae8', b'fb08', b'fb28', b'fb48', b'fb68', b'fb88', b'fba8', b'fbd0', b'fbf0',
                    b'fc10', b'fc30', b'fc50', b'fc70', b'fc90', b'fcb0', b'fcd0', b'fcf0', b'fd10', b'fd38', b'fd58',
                    b'fd78', b'fd98', b'fdb8', b'fdd8', b'fdf8', b'fe18', b'fe38', b'fe58', b'fe80', b'fea0', b'fec0',
                    b'fee0', b'ff00', b'ff20', b'ff40', b'ff60', b'ff80', b'ffa0', b'ffc0', b'ffe8']
        azimuth = str(azimuths[azimuthCount])[2:-1]
        azimuthCount = azimuthCount + 1
        videoRecordHeader = videoRecordHeader + 1
        videoRecordHeaderBytes = videoRecordHeader.to_bytes(4, 'big')
        videoRecordHeaderBytes = str(binascii.hexlify(videoRecordHeaderBytes))[2:-1]

        message = str(message)[2:18] + videoRecordHeaderBytes + azimuth + azimuth + str(message)[34:-1]
        message = binascii.a2b_hex(message)
        self.sock.sendto(message, (MCAST_GRP, MCAST_PORT))

    def discoveryThread(self, discoveryFlag=True):
        # discovery = b'6473706e6f723a20762e303030300a3139322e3136382e312e3232323a35393632330a0000000000'  # 192.168.1.222
        discovery = b'6473706e6f723a20762e303030300a31302e3132392e312e33343a35393632330a0000000000'  # 10.129.1.34
        discovery = binascii.a2b_hex(discovery)

        self.sock.sendto(discovery, ('227.228.229.230', 59368))
        time.sleep(1)
        if discoveryFlag:
            threading.Thread(target=self.discoveryThread).start()
