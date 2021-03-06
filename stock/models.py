#import uuid #제일 위에 위치시켜야 함
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection

class StockList(models.Model):
    user_id = models.PositiveIntegerField()
    company_id = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    use_yn = models.CharField(max_length=1, blank=True, null=True)
    rmk = models.CharField(max_length=200, blank=True, null=True)
    upd_d = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_list'

    #def get_absolute_url(self):
     #   return reverse('stockList') #args=[str(self.id)]


class StockPrice(models.Model):
    company_id = models.CharField(max_length=30, blank=True, null=True)
    txn_date = models.DateField()
    price_open = models.FloatField(blank=True, null=True)
    price_high = models.FloatField(blank=True, null=True)
    price_low = models.FloatField(blank=True, null=True)
    price_close = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    volume_foreign = models.FloatField(blank=True, null=True)
    volume_org = models.FloatField(blank=True, null=True)
    per = models.FloatField(blank=True, null=True)
    eps = models.FloatField(blank=True, null=True)
    pbr = models.FloatField(blank=True, null=True)
    risefall = models.FloatField(blank=True, null=True)
    risefall_rate = models.FloatField(blank=True, null=True)
    fcst = models.IntegerField(blank=True, null=True)
    #residual = models.IntegerField(blank=True, null=True)
    upd_d = models.DateTimeField(blank=True, null=True)
    price_avg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_price'

    def __str__(self):  # dunder method(double underscore)
        return "종목코드: " + self.company_id

class Book(models.Model):
   # id = models.UUIDField(
    #    primary_key=True,
     #   default=uuid.uuid4,
      #  editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    cover = models.ImageField(upload_to='covers/', blank=True)

    class Meta:
        permissions = [
            ("special_status", "Can read all books"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    review = models.CharField(max_length=255)

    def __str__(self):
        return self.review

class StockIndicator(models.Model):
    company_id = models.CharField(max_length=30, blank=True, null=True)
    txn_date = models.DateField(blank=True, null=True)
    c_engulf = models.CharField(max_length=1, blank=True, null=True)
    c_three_method = models.CharField(max_length=1, blank=True, null=True)
    c_two_medium = models.CharField(max_length=1, blank=True, null=True)
    c_gap = models.CharField(max_length=1, blank=True, null=True)
    c_red3 = models.CharField(max_length=1, blank=True, null=True)
    ma5 = models.FloatField(blank=True, null=True)
    ma10 = models.FloatField(blank=True, null=True)
    ma20 = models.FloatField(blank=True, null=True)
    ma60 = models.FloatField(blank=True, null=True)
    ma120 = models.FloatField(blank=True, null=True)
    ema12 = models.FloatField(blank=True, null=True)
    ema26 = models.FloatField(blank=True, null=True)
    typical_price = models.FloatField(blank=True, null=True)
    sto_f_k = models.FloatField(blank=True, null=True)
    sto_f_d = models.FloatField(blank=True, null=True)
    sto_s_k = models.FloatField(blank=True, null=True)
    sto_s_d = models.FloatField(blank=True, null=True)
    sto_gd = models.CharField(max_length=1, blank=True, null=True)
    macd = models.FloatField(blank=True, null=True)
    macd_signal = models.FloatField(blank=True, null=True)
    macd_oscill = models.FloatField(blank=True, null=True)
    rsi = models.FloatField(blank=True, null=True)
    rsi_signal = models.FloatField(blank=True, null=True)
    ilmok_convert = models.FloatField(blank=True, null=True)
    ilmok_base = models.FloatField(blank=True, null=True)
    ilmok_back_span = models.FloatField(blank=True, null=True)
    ilmok_span1 = models.FloatField(blank=True, null=True)
    ilmok_span2 = models.FloatField(blank=True, null=True)
    ilmok_gd = models.CharField(max_length=1, blank=True, null=True)
    bb_upper = models.FloatField(blank=True, null=True)
    bb_lower = models.FloatField(blank=True, null=True)
    bb_gd = models.CharField(max_length=1, blank=True, null=True)
    investor_sent = models.FloatField(blank=True, null=True)
    investor_sent_signal = models.FloatField(blank=True, null=True)
    disparity = models.FloatField(blank=True, null=True)
    adl = models.FloatField(blank=True, null=True)
    co_ema3 = models.FloatField(blank=True, null=True)
    co_ema10 = models.FloatField(blank=True, null=True)
    co = models.IntegerField(blank=True, null=True)
    co_signal = models.IntegerField(blank=True, null=True)
    momentum = models.FloatField(blank=True, null=True)
    momentum_signal = models.FloatField(blank=True, null=True)
    momentum_gd = models.CharField(max_length=1, blank=True, null=True)
    yield_gap = models.FloatField(blank=True, null=True)
    slope = models.FloatField(blank=True, null=True)
    slope20 = models.FloatField(blank=True, null=True)
    slope120 = models.FloatField(blank=True, null=True)
    ev_ebitda = models.FloatField(blank=True, null=True)
    per = models.FloatField(blank=True, null=True)
    arima = models.FloatField(blank=True, null=True)
    pvi = models.FloatField(blank=True, null=True)
    pvi_signal = models.FloatField(blank=True, null=True)
    nvi = models.FloatField(blank=True, null=True)
    obv = models.FloatField(blank=True, null=True)
    obv_signal = models.FloatField(blank=True, null=True)
    obv_gd = models.CharField(max_length=1, blank=True, null=True)
    obv_org = models.FloatField(blank=True, null=True)
    obv_frn = models.FloatField(blank=True, null=True)
    nvi_signal = models.FloatField(blank=True, null=True)
    sonar = models.FloatField(blank=True, null=True)
    sonar_signal = models.FloatField(blank=True, null=True)
    dx_pdm = models.FloatField(blank=True, null=True)
    dx_mdm = models.FloatField(blank=True, null=True)
    dx_trm = models.FloatField(blank=True, null=True)
    dx_pdi = models.FloatField(blank=True, null=True)
    dx_mdi = models.FloatField(blank=True, null=True)
    dx_gd = models.CharField(max_length=1, blank=True, null=True)
    adx_dx = models.FloatField(blank=True, null=True)
    adx = models.FloatField(blank=True, null=True)
    cciy = models.FloatField(blank=True, null=True)
    cci = models.FloatField(blank=True, null=True)
    formula = models.FloatField(blank=True, null=True)
    mfi_pos = models.FloatField(blank=True, null=True)
    mfi_neg = models.FloatField(blank=True, null=True)
    mfi = models.FloatField(blank=True, null=True)
    wo_ad = models.FloatField(blank=True, null=True)
    wo = models.FloatField(blank=True, null=True)
    wo_signal = models.FloatField(blank=True, null=True)
    investor_sent_new = models.FloatField(blank=True, null=True)
    elder_ray_bull = models.FloatField(blank=True, null=True)
    elder_ray_bear = models.FloatField(blank=True, null=True)
    sigma = models.FloatField(blank=True, null=True)
    maxmin10 = models.FloatField(blank=True, null=True)
    maxmin20 = models.FloatField(blank=True, null=True)
    ema10 = models.FloatField(blank=True, null=True)
    ema5 = models.FloatField(blank=True, null=True)
    ema20 = models.FloatField(blank=True, null=True)
    dema5 = models.FloatField(blank=True, null=True)
    dema20 = models.FloatField(blank=True, null=True)
    ema9_diff = models.FloatField(blank=True, null=True)
    dema9_diff = models.FloatField(blank=True, null=True)
    mass_index = models.FloatField(blank=True, null=True)
    mass_index_signal = models.FloatField(blank=True, null=True)
    price_oscill = models.FloatField(blank=True, null=True)
    price_oscill_signal = models.FloatField(blank=True, null=True)
    pvt = models.FloatField(blank=True, null=True)
    pvt_signal = models.FloatField(blank=True, null=True)
    aroon_up = models.FloatField(blank=True, null=True)
    aroon_down = models.FloatField(blank=True, null=True)
    aroon_gd = models.CharField(max_length=1, blank=True, null=True)
    psar_up = models.FloatField(blank=True, null=True)
    psar_down = models.FloatField(blank=True, null=True)
    psar_gd = models.CharField(max_length=1, blank=True, null=True)
    dx_pdm_e = models.FloatField(blank=True, null=True)
    dx_mdm_e = models.FloatField(blank=True, null=True)
    dx_trm_e = models.FloatField(blank=True, null=True)
    c_pole = models.CharField(max_length=1, blank=True, null=True)
    cmf_ad = models.FloatField(blank=True, null=True)
    cmf = models.FloatField(blank=True, null=True)
    demark_support = models.FloatField(blank=True, null=True)
    demark_resistance = models.FloatField(blank=True, null=True)
    demark_base = models.FloatField(blank=True, null=True)
    mac1 = models.FloatField(blank=True, null=True)
    mac2 = models.FloatField(blank=True, null=True)
    mac3 = models.FloatField(blank=True, null=True)
    mac4 = models.FloatField(blank=True, null=True)
    rsi_macd1 = models.FloatField(blank=True, null=True)
    rsi_macd2 = models.FloatField(blank=True, null=True)
    rsi_macd = models.FloatField(blank=True, null=True)
    rsi_macd_signal = models.FloatField(blank=True, null=True)
    sonar_sent = models.IntegerField(blank=True, null=True)
    sonar_sent_signal = models.FloatField(blank=True, null=True)
    rvi = models.FloatField(blank=True, null=True)
    upd_d = models.DateTimeField(blank=True, null=True)
    sim = models.FloatField(blank=True, null=True)
    c_reversal = models.CharField(max_length=1, blank=True, null=True)
    c_thrust = models.CharField(max_length=1, blank=True, null=True)
    spike_day = models.CharField(max_length=1, blank=True, null=True)
    c_island = models.CharField(max_length=1, blank=True, null=True)
    c_star = models.CharField(max_length=20, blank=True, null=True)
    c_doji = models.CharField(max_length=1, blank=True, null=True)
    hammer_type = models.CharField(max_length=2, blank=True, null=True)
    c_hammer3 = models.CharField(max_length=1, blank=True, null=True)
    c_harami = models.CharField(max_length=1, blank=True, null=True)
    pyramid = models.CharField(max_length=15, blank=True, null=True)
    body_length_avg = models.IntegerField(blank=True, null=True)
    c_belthold = models.CharField(max_length=1, blank=True, null=True)
    c_length_avg = models.IntegerField(blank=True, null=True)
    true_range = models.IntegerField(blank=True, null=True)
    c_spinning = models.CharField(max_length=1, blank=True, null=True)
    c_pierce = models.CharField(max_length=1, blank=True, null=True)
    ma_stratum = models.CharField(max_length=1, blank=True, null=True)
    t3 = models.FloatField(blank=True, null=True)
    price_ch_upper = models.FloatField(blank=True, null=True)
    price_ch_lower = models.FloatField(blank=True, null=True)
    price_ch = models.CharField(max_length=1, blank=True, null=True)
    ema_double5 = models.FloatField(blank=True, null=True)
    ema_double20 = models.FloatField(blank=True, null=True)
    ema_triple5 = models.FloatField(blank=True, null=True)
    ema_triple20 = models.FloatField(blank=True, null=True)
    tema5 = models.FloatField(blank=True, null=True)
    tema20 = models.FloatField(blank=True, null=True)
    c_qstick = models.FloatField(blank=True, null=True)
    c_qstick_signal = models.FloatField(blank=True, null=True)
    stoch_rsi_k = models.FloatField(blank=True, null=True)
    stoch_rsi_d = models.FloatField(blank=True, null=True)
    cmo = models.FloatField(blank=True, null=True)
    kvo_cm = models.FloatField(blank=True, null=True)
    kvo_vf = models.FloatField(blank=True, null=True)
    kvo = models.FloatField(blank=True, null=True)
    kvo_signal = models.FloatField(blank=True, null=True)
    true_low = models.FloatField(blank=True, null=True)
    ultimate_oscill = models.FloatField(blank=True, null=True)
    will_percent_r = models.FloatField(blank=True, null=True)
    will_percent_r_signal = models.FloatField(blank=True, null=True)
    binary_wave = models.IntegerField(blank=True, null=True)
    fcst_oscill = models.FloatField(blank=True, null=True)
    lsma14 = models.FloatField(blank=True, null=True)
    fcst_oscill_signal = models.FloatField(blank=True, null=True)
    pvo = models.FloatField(blank=True, null=True)
    pvo_signal = models.FloatField(blank=True, null=True)
    vema5 = models.FloatField(blank=True, null=True)
    vema20 = models.FloatField(blank=True, null=True)
    vo = models.FloatField(blank=True, null=True)
    force_index = models.FloatField(blank=True, null=True)
    csi = models.FloatField(blank=True, null=True)
    projection_upper = models.FloatField(blank=True, null=True)
    projection_lower = models.FloatField(blank=True, null=True)
    smi_cm_ema = models.FloatField(blank=True, null=True)
    smi_hl_ema = models.FloatField(blank=True, null=True)
    smi_cm = models.FloatField(blank=True, null=True)
    smi_hl = models.FloatField(blank=True, null=True)
    smi = models.FloatField(blank=True, null=True)
    smi_signal = models.FloatField(blank=True, null=True)
    inertia = models.FloatField(blank=True, null=True)
    inertia_signal = models.FloatField(blank=True, null=True)
    vidya = models.FloatField(blank=True, null=True)
    vidya_signal = models.FloatField(blank=True, null=True)
    projection_oscill = models.FloatField(blank=True, null=True)
    projection_oscill_signal = models.FloatField(blank=True, null=True)
    dynamic_mi = models.IntegerField(blank=True, null=True)
    tema5_signal = models.FloatField(blank=True, null=True)
    trix = models.IntegerField(blank=True, null=True)
    lsma7 = models.FloatField(blank=True, null=True)
    ma_gd = models.CharField(max_length=1, blank=True, null=True)
    c_scare = models.CharField(max_length=1, blank=True, null=True)
    volume_sent = models.FloatField(blank=True, null=True)
    vol_ma20 = models.FloatField(blank=True, null=True)
    trend_fcst = models.FloatField(blank=True, null=True)
    pattern_w = models.CharField(max_length=1, blank=True, null=True)
    pattern_w_price = models.FloatField(blank=True, null=True)
    pattern_w_info = models.CharField(max_length=100, blank=True, null=True)
    price_resist = models.IntegerField(blank=True, null=True)
    price_support = models.IntegerField(blank=True, null=True)
    c_zigzag = models.CharField(max_length=1, blank=True, null=True)
    mesa_sine = models.FloatField(blank=True, null=True)
    mesa_leadsine = models.FloatField(blank=True, null=True)
    cv = models.IntegerField(blank=True, null=True)
    slope5 = models.FloatField(blank=True, null=True)
    mesa_phase = models.FloatField(blank=True, null=True)
    vol_price_ma5 = models.FloatField(blank=True, null=True)
    vol_price_ma20 = models.FloatField(blank=True, null=True)
    adxr = models.FloatField(blank=True, null=True)
    vhf = models.FloatField(blank=True, null=True)
    lrs = models.FloatField(blank=True, null=True)
    lrs_signal = models.FloatField(blank=True, null=True)
    pfe_pre = models.FloatField(blank=True, null=True)
    pfe = models.FloatField(blank=True, null=True)
    dpo = models.FloatField(blank=True, null=True)
    dpo_signal = models.FloatField(blank=True, null=True)
    is_pattern_flag = models.IntegerField(blank=True, null=True)
    pattern_flag_info = models.CharField(max_length=200, blank=True, null=True)
    pattern_type = models.CharField(max_length=1, blank=True, null=True)
    pattern_flag_high = models.FloatField(blank=True, null=True)
    pattern_flag_low = models.FloatField(blank=True, null=True)
    csi_rank = models.IntegerField(blank=True, null=True)
    volume_liquidate = models.CharField(max_length=1, blank=True, null=True)
    vol_ma20_org = models.FloatField(blank=True, null=True)
    ma60_gd = models.CharField(max_length=1, blank=True, null=True)
    trend_code = models.CharField(max_length=1, blank=True, null=True)
    upper_today = models.FloatField(blank=True, null=True)
    lower_today = models.FloatField(blank=True, null=True)
    trend_upper_info = models.CharField(max_length=255, blank=True, null=True)
    trend_lower_info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_indicator'


class StockTxn(models.Model):
    txn_seq = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField(blank=True, null=True)
    bos = models.CharField(max_length=1, blank=True, null=True)
    txn_date = models.DateField(blank=True, null=True)
    txn_time = models.DateTimeField(blank=True, null=True)
    company_id = models.CharField(max_length=10)
    txn_yn = models.CharField(max_length=1, blank=True, null=True)
    reset_yn = models.CharField(max_length=1, blank=True, null=True)
    close_yn = models.CharField(max_length=1, blank=True, null=True)
    txn_qty = models.IntegerField(blank=True, null=True)
    txn_price = models.IntegerField(blank=True, null=True)
    txn_fee = models.IntegerField(blank=True, null=True)
    cash_inout = models.IntegerField(blank=True, null=True)
    cash_balance = models.IntegerField(blank=True, null=True)
    asis_price = models.IntegerField(blank=True, null=True)
    target_period = models.IntegerField(blank=True, null=True)
    target_price = models.IntegerField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    bos_reason = models.CharField(max_length=100, blank=True, null=True)
    bos_reason_detail = models.CharField(max_length=250, blank=True, null=True)
    result_review = models.CharField(max_length=250, blank=True, null=True)
    upd_d = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_txn'

class StockChangeHis(models.Model):
    txn_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    rmk = models.CharField(max_length=200, blank=True, null=True)
    upd_d = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_change_his'


class StockCompany(models.Model):
    company_id = models.CharField(max_length=10)
    company_name = models.CharField(max_length=30)
    pod = models.CharField(max_length=1)
    baedang = models.CharField(max_length=1, blank=True, null=True)
    dom_yn = models.CharField(max_length=1, blank=True, null=True)
    cre_d = models.DateTimeField(blank=True, null=True)
    corr_oil = models.FloatField(blank=True, null=True)
    corr_exchange = models.FloatField(blank=True, null=True)
    corr_interest = models.FloatField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_company'

    def get_absolute_url(self):
        return reverse('stockCompany', args=[str(self.id)]) # 뷰에서 success_url = reverse_lazy('stockCompany') 하는 것과 동일


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        #return reverse('stock:item_in_category', args=[self.slug])   # stock: 는 namespace를 의미함.
        #return reverse('item_in_category', args=[self.slug])
        return reverse('item_in_category', args=[str(self.id)])

class StockScoreMaster(models.Model):
    #category = models.CharField(max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    item = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='items/%Y/%m/%d', blank=True)
    item_desc = models.CharField(max_length=250)
    long_desc = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(blank=True)

    def_field = models.TextField(db_column='def', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    plus = models.CharField(max_length=250, blank=True, null=True)
    minus = models.CharField(max_length=250, blank=True, null=True)
    criteria1 = models.FloatField(blank=True, null=True)
    criteria1_desc = models.CharField(max_length=200, blank=True, null=True)
    criteria2 = models.FloatField(blank=True, null=True)
    criteria2_desc = models.CharField(max_length=200, blank=True, null=True)
    use_yn = models.CharField(max_length=1)
    image_name = models.CharField(max_length=100, blank=True, null=True)
    time_delay = models.IntegerField(blank=True, null=True)
    seq_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_score_master'
        index_together = [['id', 'item']]

    def __str__(self):
        return self.item

    def get_absolute_url(self):
        return reverse('item_detail', args=[self.id, self.slug])

"""
def TxnMonthlySQL(self):

    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM stock_txn WHERE txn_yn ="Y"''')
    #row = cursor.fetchone()
    result = cursor.fetchall()

    return result
"""


class StockTxnTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(max_length=6, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    profit = models.FloatField(blank=True, null=True)
    upd_d = models.DateField(blank=True, null=True)
    txn_fee = models.IntegerField(blank=True, null=True)
    target_yn = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_txn_temp'




class StockScoreLog(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(max_length=6, blank=True, null=True)
    txn_date = models.DateField(blank=True, null=True)
    c_hammer1 = models.IntegerField(blank=True, null=True)
    c_hammer2 = models.IntegerField(blank=True, null=True)
    c_doji = models.IntegerField(blank=True, null=True)
    c_engulf = models.IntegerField(blank=True, null=True)
    c_three_method = models.IntegerField(blank=True, null=True)
    c_two_medium = models.IntegerField(blank=True, null=True)
    c_gap = models.IntegerField(blank=True, null=True)
    c_pole = models.IntegerField(blank=True, null=True)
    ma5 = models.IntegerField(blank=True, null=True)
    ma5_20 = models.IntegerField(blank=True, null=True)
    ma5_60 = models.IntegerField(blank=True, null=True)
    ma_gd = models.IntegerField(blank=True, null=True)
    ma_gd_slope = models.IntegerField(blank=True, null=True)
    formula = models.IntegerField(blank=True, null=True)
    macd = models.IntegerField(blank=True, null=True)
    macd_gd = models.IntegerField(blank=True, null=True)
    sto = models.IntegerField(blank=True, null=True)
    sto_gd = models.IntegerField(blank=True, null=True)
    sto_up_down = models.IntegerField(blank=True, null=True)
    ilmok_cloud = models.IntegerField(blank=True, null=True)
    ilmok_layer = models.IntegerField(blank=True, null=True)
    ilmok_gd = models.IntegerField(blank=True, null=True)
    bb_band = models.IntegerField(blank=True, null=True)
    bb_direction = models.IntegerField(blank=True, null=True)
    bb_gd = models.IntegerField(blank=True, null=True)
    envelope = models.IntegerField(blank=True, null=True)
    investor_sent = models.IntegerField(blank=True, null=True)
    rsi = models.IntegerField(blank=True, null=True)
    disparity = models.IntegerField(blank=True, null=True)
    obv = models.IntegerField(blank=True, null=True)
    obv_gd = models.IntegerField(blank=True, null=True)
    momentum_gd = models.IntegerField(blank=True, null=True)
    momentum = models.IntegerField(blank=True, null=True)
    per = models.IntegerField(blank=True, null=True)
    eps = models.IntegerField(blank=True, null=True)
    pbr = models.IntegerField(blank=True, null=True)
    yield_gap = models.IntegerField(blank=True, null=True)
    obv_org = models.IntegerField(blank=True, null=True)
    ev_ebitda = models.IntegerField(blank=True, null=True)
    co = models.IntegerField(blank=True, null=True)
    macd_oscill = models.IntegerField(blank=True, null=True)
    pvi_nvi = models.IntegerField(blank=True, null=True)
    sonar_gd = models.IntegerField(blank=True, null=True)
    dx = models.IntegerField(blank=True, null=True)
    dx_gd = models.IntegerField(blank=True, null=True)
    adx = models.IntegerField(blank=True, null=True)
    hybrid1 = models.IntegerField(blank=True, null=True)
    obv_frn = models.IntegerField(blank=True, null=True)
    mix_gd = models.IntegerField(blank=True, null=True)
    cci1 = models.IntegerField(blank=True, null=True)
    cci2 = models.IntegerField(blank=True, null=True)
    mfi = models.IntegerField(blank=True, null=True)
    wo = models.IntegerField(blank=True, null=True)
    investor_sent_new = models.IntegerField(blank=True, null=True)
    elder_ray = models.IntegerField(blank=True, null=True)
    sigma = models.IntegerField(blank=True, null=True)
    keltner = models.IntegerField(blank=True, null=True)
    dema = models.IntegerField(blank=True, null=True)
    mass_index = models.IntegerField(blank=True, null=True)
    price_oscill = models.IntegerField(blank=True, null=True)
    pvt = models.IntegerField(blank=True, null=True)
    aroon_gd = models.IntegerField(blank=True, null=True)
    psar = models.IntegerField(blank=True, null=True)
    rsi_gd = models.IntegerField(blank=True, null=True)
    upd_d = models.DateTimeField(blank=True, null=True)
    cmf = models.IntegerField(blank=True, null=True)
    demark = models.IntegerField(blank=True, null=True)
    mac = models.IntegerField(blank=True, null=True)
    rsi_macd = models.IntegerField(blank=True, null=True)
    sonar_sent = models.IntegerField(blank=True, null=True)
    bb_detach = models.IntegerField(blank=True, null=True)
    rvi = models.IntegerField(blank=True, null=True)
    c_red3 = models.IntegerField(blank=True, null=True)
    sto_bull_bear = models.IntegerField(blank=True, null=True)
    c_reversal = models.IntegerField(blank=True, null=True)
    c_thrust = models.IntegerField(blank=True, null=True)
    spike_day = models.IntegerField(blank=True, null=True)
    sim = models.IntegerField(blank=True, null=True)
    c_island = models.IntegerField(blank=True, null=True)
    c_star = models.IntegerField(blank=True, null=True)
    c_hammer3 = models.IntegerField(blank=True, null=True)
    c_harami = models.IntegerField(blank=True, null=True)
    pyramid = models.IntegerField(blank=True, null=True)
    cci3 = models.IntegerField(blank=True, null=True)
    mix_divergence = models.IntegerField(blank=True, null=True)
    c_belthold = models.IntegerField(blank=True, null=True)
    c_spinning = models.IntegerField(blank=True, null=True)
    c_pierce = models.IntegerField(blank=True, null=True)
    ma_stratum = models.IntegerField(blank=True, null=True)
    t3 = models.IntegerField(blank=True, null=True)
    price_ch = models.IntegerField(blank=True, null=True)
    tema = models.IntegerField(blank=True, null=True)
    c_qstick = models.IntegerField(blank=True, null=True)
    stoch_rsi = models.IntegerField(blank=True, null=True)
    cmo = models.IntegerField(blank=True, null=True)
    kvo = models.IntegerField(blank=True, null=True)
    ultimate_oscill = models.IntegerField(blank=True, null=True)
    will_percent_r = models.IntegerField(blank=True, null=True)
    binary_wave = models.IntegerField(blank=True, null=True)
    fcst_oscill = models.IntegerField(blank=True, null=True)
    aroon = models.IntegerField(blank=True, null=True)
    adl = models.IntegerField(blank=True, null=True)
    pvo = models.IntegerField(blank=True, null=True)
    vo = models.IntegerField(blank=True, null=True)
    force_index = models.IntegerField(blank=True, null=True)
    csi = models.IntegerField(blank=True, null=True)
    projection = models.IntegerField(blank=True, null=True)
    smi = models.IntegerField(blank=True, null=True)
    inertia = models.IntegerField(blank=True, null=True)
    vidya = models.IntegerField(blank=True, null=True)
    projection_oscill = models.IntegerField(blank=True, null=True)
    sent_disparity = models.IntegerField(blank=True, null=True)
    trix = models.IntegerField(blank=True, null=True)
    c_scare = models.IntegerField(blank=True, null=True)
    volume_sent = models.IntegerField(blank=True, null=True)
    volume_liquidate = models.IntegerField(blank=True, null=True)
    trend_fcst = models.IntegerField(blank=True, null=True)
    pattern_w = models.IntegerField(blank=True, null=True)
    sonar = models.IntegerField(blank=True, null=True)
    c_zigzag = models.IntegerField(blank=True, null=True)
    spring = models.IntegerField(blank=True, null=True)
    bb_center = models.IntegerField(blank=True, null=True)
    volume_mass = models.IntegerField(blank=True, null=True)
    mesa = models.IntegerField(blank=True, null=True)
    vama = models.IntegerField(blank=True, null=True)
    adxr = models.IntegerField(blank=True, null=True)
    lrs = models.IntegerField(blank=True, null=True)
    pfe = models.IntegerField(blank=True, null=True)
    dpo = models.IntegerField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    ma60 = models.IntegerField(blank=True, null=True)
    trend_breakaway = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_score_log'



class StockYmd(models.Model):
    txn_date = models.DateField()
    index_kospi = models.FloatField(blank=True, null=True)
    index_kosdaq = models.FloatField(blank=True, null=True)
    date_seq = models.IntegerField()
    index_dow = models.FloatField(blank=True, null=True)
    index_nasdaq = models.FloatField(blank=True, null=True)
    baedang = models.CharField(max_length=1, blank=True, null=True)
    interest = models.FloatField(blank=True, null=True)
    oil = models.FloatField(blank=True, null=True)
    exchange = models.FloatField(blank=True, null=True)
    index_sp500 = models.FloatField(blank=True, null=True)
    rmk = models.CharField(max_length=200, blank=True, null=True)
    usa_open_yn = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_ymd'
