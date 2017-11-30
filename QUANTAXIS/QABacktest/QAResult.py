# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from QUANTAXIS.QAFetch.QAQuery import QA_fetch_backtest_history, QA_fetch_backtest_info
import pandas as pd
from statistics import mean




class result_analyzer():
    def __init__(self, cookie_id, *args, **kwargs):
        self.cookie = cookie_id
        self.backtest_history=QA_fetch_backtest_history(cookie=self.cookie)
        self.backtest_info=QA_fetch_backtest_info(account_cookie=self.cookie)

    @property
    def history(self):
        data=pd.DataFrame(self.backtest_history[0]['history'],columns=['datetime','code','price','towards','amounts','o_id','d_id','commission'])
        return data.drop(['o_id','d_id'],axis=1)
    
    @property
    def detail(self):
        detail=pd.DataFrame(self.backtest_history[0]['detail'],columns=['date', 'code', 'price', 'amounts', 'order_id',
                                                                                  'trade_id', 'sell_price', 'sell_order_id',
                                                                                  'sell_trade_id', 'sell_date', 'left_amount',
                                                                                  'commission'])

        detail['sell_average'] = detail['sell_price'].apply(lambda x: _mean(x))

        try:
            detail['pnl_price'] = detail['sell_average'] - \
                detail['price']

            detail['pnl'] = detail['pnl_price'] * (
                detail['amounts'] - detail['left_amount']) - detail['commission']


            detail['pnl_presentage']=detail['pnl_price']/detail['price']
        except:
            pass

        return detail.drop(
            ['order_id', 'trade_id', 'sell_order_id', 'sell_trade_id'], axis=1)

        
    @property
    def codes(self):
        return self.history.code.unique().tolist()
    
    def get_stock_tradehistory(self,code):
        return self.history[self.history.code==code]
    def get_stock_tradedetail(self,code):
        return self.detail[self.detail.code==code]
    

def _mean(list_):
    if len(list_) > 0:
        return mean(list_)
    else:
        return 'No Data'




if __name__=='__main__':
    ana=result_analyzer(cookie_id='0.0792467630583924')
    print(ana.detail)
    code=ana.codes
    print(ana.get_stock_tradehistory(code[1]))
    print(ana.get_stock_tradedetail(code[1]))