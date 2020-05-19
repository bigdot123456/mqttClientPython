# coding: utf-8
from sqlalchemy import Column, DateTime, Float, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    name = Column(String(32))
    id = Column(BIGINT(20), primary_key=True)
    password = Column(String(40), nullable=False)
    right = Column(INTEGER(11))


class AppVersion(Base):
    __tablename__ = 'app_version'

    id = Column(BIGINT(20), primary_key=True)
    version = Column(String(8))
    log = Column(String(2048))
    timestamp = Column(BIGINT(20))
    type = Column(String(16))
    token = Column(String(64))


class AssetBase(Base):
    __tablename__ = 'asset_base'

    id = Column(BIGINT(20), primary_key=True, nullable=False)
    phone = Column(String(32), primary_key=True, nullable=False, comment='account phone')
    ethaddress = Column(String(42), comment='eth address')
    tokenbalance = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"), comment='token balance')
    usdtbalance = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"), comment='usdt 余额')
    lockbalance = Column(Float(asdecimal=True), server_default=text("'0'"))
    tokenaddress = Column(String(42))
    macbalance = Column(Float(asdecimal=True), server_default=text("'0'"))


class AssetCheckresultpython(Base):
    __tablename__ = 'asset_checkresultpython'

    id = Column(INTEGER(11), primary_key=True)
    phone = Column(String(32), nullable=False, comment='phone number')
    paypassword = Column(String(64), comment='pay password')
    registertime = Column(BIGINT(20), comment='register time')
    countryCode = Column(String(8))
    signtime = Column(BIGINT(20))
    ethaddress = Column(String(42), comment='eth address')
    tokenbalance = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"), comment='token balance')
    usdtbalance = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"), comment='usdt 余额')
    lockbalance = Column(Float(asdecimal=True), server_default=text("'0'"))
    tokenaddress = Column(String(42))
    macbalance = Column(Float(asdecimal=True), server_default=text("'0'"))
    name = Column(String(20), comment='username ')
    email = Column(String(32), comment='email address')
    password = Column(String(64), comment='md5 of password')
    code = Column(String(10), comment='invitation code')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='0、未激活 1、运行、2淘汰')
    fundtype = Column(INTEGER(4), server_default=text("'0'"), comment='基金类型')
    userid = Column(String(32), nullable=False, comment='用户id')
    starttime = Column(BIGINT(20), nullable=False, comment='购买矿机时间')
    stoptime = Column(BIGINT(20), server_default=text("'0'"), comment='退租矿机时间')
    lastdayinterest = Column(Float(asdecimal=True), server_default=text("'0'"))
    gas = Column(Float(asdecimal=True), server_default=text("'0'"))
    attribute = Column(String(1024), comment='矿机属性')
    production = Column(Float(20, True), server_default=text("'0.0000'"))
    updatetime = Column(BIGINT(20), server_default=text("'0'"))
    mycodeID = Column(INTEGER(11), nullable=False, comment='mycode 排序索引')
    mycode = Column(String(10), comment='my invitation code')
    fund = Column(Float(asdecimal=True), server_default=text("'0'"), comment='本金')
    mycodeIDSubListIndex = Column(String(1024), comment='mycode 直接下属的排序索引,通过逗号分割')
    mycodeIDGrandSonListIndex = Column(String(1024), comment='mycode 二级直接下属的排序索引,通过逗号分割')
    mycodeIDsubNodevipLevelIndex = Column(String(32), comment='VIP下属层级编号')
    recommend = Column(Float(asdecimal=True), server_default=text("'0'"))
    circle = Column(Float(asdecimal=True))
    vipTreeBalance = Column(Float, server_default=text("'0'"), comment='vip计算的领主金额')
    vipTag = Column(INTEGER(11), server_default=text("'0'"), comment='vip标志')
    vipLevel = Column(INTEGER(11), server_default=text("'0'"), comment='vip等级')
    usedBalance = Column(Float, server_default=text("'0'"), comment='用户用于真实计算的金额')
    minerProductive = Column(Float, server_default=text("'0'"), comment='矿机系数')
    staticIncome = Column(Float)
    staticIncomeTree = Column(Float)
    MinerAward = Column(Float)
    RecommendAward = Column(Float)
    Recommend1Award = Column(Float)
    Recommend2Award = Column(Float)
    DynamicAward = Column(Float)
    TotalAward = Column(Float)
    static = Column(Float(asdecimal=True), server_default=text("'0'"), comment='静态利息')
    dynamic = Column(Float(asdecimal=True), server_default=text("'0'"), comment='动态利息')
    decription = Column(String(4096), comment='用于说明计算过程')


class AssetFund(Base):
    __tablename__ = 'asset_fund'

    id = Column(BIGINT(8), primary_key=True)
    fund = Column(Float(asdecimal=True), server_default=text("'0'"), comment='本金')
    static = Column(Float(asdecimal=True), server_default=text("'0'"), comment='静态利息')
    recommend = Column(Float(asdecimal=True))
    circle = Column(Float(asdecimal=True))
    dynamic = Column(Float(asdecimal=True), server_default=text("'0'"), comment='动态利息')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='0、未激活 1、运行、2淘汰')
    fundtype = Column(INTEGER(4), server_default=text("'0'"), comment='基金类型')
    userid = Column(String(32), nullable=False, comment='用户id')
    starttime = Column(BIGINT(20), nullable=False, comment='购买矿机时间')
    stoptime = Column(BIGINT(20), server_default=text("'0'"), comment='退租矿机时间')
    lastdayinterest = Column(Float(asdecimal=True), server_default=text("'0'"))
    gas = Column(Float(asdecimal=True), server_default=text("'0'"))
    attribute = Column(String(1024), comment='矿机属性')
    production = Column(Float(20, True), server_default=text("'0.0000'"))
    updatetime = Column(BIGINT(20), server_default=text("'0'"))


class AssetLoadsqldatum(Base):
    __tablename__ = 'asset_loadsqldata'

    id = Column(INTEGER(11), primary_key=True)
    phone = Column(String(32), nullable=False, comment='phone number')
    paypassword = Column(String(64), comment='pay password')
    registertime = Column(BIGINT(20), comment='register time')
    countryCode = Column(String(8))
    signtime = Column(BIGINT(20))
    ethaddress = Column(String(42), comment='eth address')
    tokenbalance = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"), comment='token balance')
    usdtbalance = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"), comment='usdt 余额')
    lockbalance = Column(Float(asdecimal=True), server_default=text("'0'"))
    tokenaddress = Column(String(42))
    macbalance = Column(Float(asdecimal=True), server_default=text("'0'"))
    name = Column(String(20), comment='username ')
    email = Column(String(32), comment='email address')
    password = Column(String(64), comment='md5 of password')
    code = Column(String(10), comment='invitation code')
    mycode = Column(String(10), comment='my invitation code')
    recommend = Column(Float(asdecimal=True), server_default=text("'0'"))
    circle = Column(Float(asdecimal=True))
    fund = Column(Float(asdecimal=True), server_default=text("'0'"), comment='本金')
    static = Column(Float(asdecimal=True), server_default=text("'0'"), comment='静态利息')
    dynamic = Column(Float(asdecimal=True), server_default=text("'0'"), comment='动态利息')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='0、未激活 1、运行、2淘汰')
    fundtype = Column(INTEGER(4), server_default=text("'0'"), comment='基金类型')
    userid = Column(String(32), nullable=False, comment='用户id')
    starttime = Column(BIGINT(20), nullable=False, comment='购买矿机时间')
    stoptime = Column(BIGINT(20), server_default=text("'0'"), comment='退租矿机时间')
    lastdayinterest = Column(Float(asdecimal=True), server_default=text("'0'"))
    gas = Column(Float(asdecimal=True), server_default=text("'0'"))
    attribute = Column(String(1024), comment='矿机属性')
    production = Column(Float(20, True), server_default=text("'0.0000'"))
    updatetime = Column(BIGINT(20), server_default=text("'0'"))


class BillCoin(Base):
    __tablename__ = 'bill_coin'

    id = Column(BIGINT(20), primary_key=True)
    timestamp = Column(BIGINT(20), server_default=text("'0'"), comment='time')
    userid = Column(VARCHAR(32))
    type = Column(INTEGER(11), server_default=text("'0'"), comment='1、充币 2、提币 3、购买基金 4、取出本金、5、收益转入')
    coin = Column(Float(20, True), server_default=text("'0'"), comment='数量')
    usdt = Column(Float(20, True), server_default=text("'0.000000'"), comment='usdt 数量')
    fee = Column(Float(20, True), server_default=text("'0.000000'"), comment='手续费')
    price = Column(Float(20, True), server_default=text("'0'"), comment='当时价格')
    ordernum = Column(String(32))
    fromaccount = Column(String(42))
    toaccount = Column(String(42))
    txhash = Column(String(66))
    status = Column(TINYINT(1), comment='0待审核，1已审核，2已转账，3取消')
    checkedtime = Column(BIGINT(20))
    sendtime = Column(BIGINT(20))


class BillFund(Base):
    __tablename__ = 'bill_fund'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(INTEGER(4), comment='1买入2取出')
    timestamp = Column(BIGINT(20), server_default=text("'0'"), comment='时间')
    value = Column(Float(11, True), server_default=text("'0'"), comment='金额')
    userid = Column(String(32), comment='用户id')
    status = Column(TINYINT(2), server_default=text("'0'"), comment='状态')
    ordernum = Column(String(32))


class BillInterest(Base):
    __tablename__ = 'bill_interest'

    id = Column(BIGINT(20), primary_key=True)
    userid = Column(BIGINT(20))
    type = Column(TINYINT(4), server_default=text("'0'"), comment='1、静态收益 2、动态收益')
    timestamp = Column(BIGINT(20), server_default=text("'0'"))
    value = Column(Float(asdecimal=True), server_default=text("'0'"))


class CoinUsdt(Base):
    __tablename__ = 'coin_usdt'

    id = Column(BIGINT(20), primary_key=True)
    timestamp = Column(BIGINT(20))
    usdt = Column(Float(asdecimal=True))


class Dbtable(Base):
    __tablename__ = 'dbtable'

    nid = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), server_default=text("'bigdot'"))
    email = Column(String(255))


class DigitAccount(Base):
    __tablename__ = 'digit_account'

    tokenaddress = Column(String(42))
    ethaddress = Column(String(42))
    privatekey = Column(String(64), primary_key=True)


class DigitAddres(Base):
    __tablename__ = 'digit_address'

    id = Column(INTEGER(11), primary_key=True)
    address = Column(String(42))
    phone = Column(String(32))


class Fund(Base):
    __tablename__ = 'fund'

    id = Column(INTEGER(11), primary_key=True)
    price = Column(Float(11, True), comment='矿机价格')
    rate = Column(Float(11, True), server_default=text("'0.000000'"), comment='矿机预期收益率/月')
    timestamp = Column(BIGINT(20), comment='更新时间')
    desc = Column(String(512), comment='描述')
    number = Column(String(20), comment='编号')
    power = Column(INTEGER(11), comment='算力 T')
    life = Column(INTEGER(11), comment='寿命 天')
    gas = Column(INTEGER(4), comment='激活矿机需要的MAN')
    production = Column(INTEGER(4), server_default=text("'0'"), comment='总产量')


class Macblockinfo(Base):
    __tablename__ = 'macblockinfo'

    blocknum = Column(BIGINT(20), primary_key=True)
    index = Column(BIGINT(20))
    timestamp = Column(DateTime)
    winner = Column(String(255))
    winnHash = Column(String(64))
    winnerAward = Column(INTEGER(11))
    onlineAward = Column(Float)
    proof = Column(BIGINT(20))
    previoushash = Column(BIGINT(20))
    transactions = Column(String(8192))


class Macmessagetable(Base):
    __tablename__ = 'macmessagetable'

    id = Column(BIGINT(20), primary_key=True)
    clientID = Column(String(32))
    time = Column(DateTime)
    topic = Column(String(128))
    message = Column(String(1024))


class Mymacnode(Base):
    __tablename__ = 'mymacnode'

    ID = Column(INTEGER(11), primary_key=True)
    Address = Column(String(32), nullable=False, server_default=text("'MAN.11111111111s'"))
    Balance = Column(INTEGER(11), server_default=text("'0'"))
    parentID = Column(INTEGER(11))
    parentAddress = Column(String(32))
    name = Column(String(32), server_default=text("'MACMAN'"))
    tel = Column(String(11), server_default=text("'13800138000'"))
    email = Column(String(64))
    attendRound = Column(INTEGER(11))
    NodeLevel = Column(INTEGER(11))
    TreeBalance = Column(Float)
    vipTreeBalance = Column(Float)
    vipTag = Column(INTEGER(11))
    vipLevel = Column(INTEGER(11))
    usedBalance = Column(Float)
    minerProductive = Column(Float)
    staticIncome = Column(Float)
    staticIncomeTree = Column(Float)
    MinerAward = Column(Float)
    RecommendAward = Column(Float)
    TotalAward = Column(Float)
    withdrawStatus = Column(INTEGER(11))


class Mymacnoderesult(Base):
    __tablename__ = 'mymacnoderesult'

    ID = Column(INTEGER(11), primary_key=True)
    Address = Column(String(32), nullable=False, server_default=text("'MAN.11111111111s'"))
    Balance = Column(INTEGER(11), server_default=text("'0'"))
    parentID = Column(INTEGER(11))
    parentAddress = Column(String(32))
    name = Column(String(32), server_default=text("'MACMAN'"))
    tel = Column(String(11), server_default=text("'13800138000'"))
    email = Column(String(64))
    attendRound = Column(INTEGER(11))
    NodeLevel = Column(INTEGER(11))
    TreeBalance = Column(Float)
    vipTreeBalance = Column(Float)
    vipTag = Column(INTEGER(11))
    vipLevel = Column(INTEGER(11))
    usedBalance = Column(Float)
    minerProductive = Column(Float)
    staticIncome = Column(Float)
    staticIncomeTree = Column(Float)
    MinerAward = Column(Float)
    RecommendAward = Column(Float)
    TotalAward = Column(Float)
    withdrawStatus = Column(INTEGER(11))


class News(Base):
    __tablename__ = 'news'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(64))
    content = Column(String(2048))
    url = Column(String(256))
    picurl = Column(String(256))
    order = Column(TINYINT(2))
    timestamp = Column(BIGINT(20))
    status = Column(TINYINT(2))


class Notice(Base):
    __tablename__ = 'notice'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(64))
    content = Column(String(2048))
    timestamp = Column(BIGINT(20))


class Principal(Base):
    __tablename__ = 'principal'

    id = Column(INTEGER(11), primary_key=True)
    fund = Column(Float(asdecimal=True), server_default=text("'0'"))
    timestamp = Column(BIGINT(20), server_default=text("'0'"))
    userid = Column(String(32))


class Scanblock(Base):
    __tablename__ = 'scanblock'

    id = Column(BIGINT(20), primary_key=True)
    startblock = Column(BIGINT(20))
    endblock = Column(BIGINT(20))
    timestamp = Column(BIGINT(20), server_default=text("'0'"))


class TxsCoin(Base):
    __tablename__ = 'txs_coin'

    id = Column(BIGINT(20), primary_key=True)
    hash = Column(String(66))
    timestamp = Column(BIGINT(20), index=True)
    value = Column(Float(20, True))
    fromaccount = Column(String(42))
    toaccount = Column(String(42))
    status = Column(TINYINT(2), server_default=text("'0'"))
    blocknum = Column(BIGINT(20))
    contract = Column(String(42))


class User(Base):
    __tablename__ = 'user'

    name = Column(String(20), comment='username ')
    phone = Column(String(32), nullable=False, comment='phone number')
    email = Column(String(32), comment='email address')
    password = Column(String(64), comment='md5 of password')
    code = Column(String(10), comment='invitation code')
    mycode = Column(String(10), comment='my invitation code')
    id = Column(INTEGER(11), primary_key=True)
    paypassword = Column(String(64), comment='pay password')
    status = Column(TINYINT(4), comment='account status')
    registertime = Column(BIGINT(20), comment='register time')
    countryCode = Column(String(8))
    signtime = Column(BIGINT(20))
    locked = Column(TINYINT(4), server_default=text("'0'"), comment='用户是否被锁定，锁定用户无法提现及转让')


class Verification(Base):
    __tablename__ = 'verification'

    phone = Column(String(32), primary_key=True)
    verification = Column(String(10))
    timestamp = Column(String(32))
