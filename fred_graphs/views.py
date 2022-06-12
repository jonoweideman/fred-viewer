from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FREDForm
import nasdaqdatalink
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
from matplotlib.ticker import LinearLocator
import matplotlib.dates as mdates



def home(request):
    if request.method == 'POST':
        form = FREDForm(request.POST)
        if form.is_valid():
            series = form.cleaned_data.get('series')
        
            print("Attempting to fetch data")
            df = nasdaqdatalink.get(f'FRED/{series}')
            print(df.head())
            df = df.reset_index()
            # df.set_index(['Date'],inplace=True)
            print(df.head())
            plot = df.plot(x='Date', y='Value', kind='scatter')

            days = ['1997-01-01', '1997-02-01']
            counts = ['30', '40']

            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(days, counts, '--bo')

            fig.autofmt_xdate()
            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
            ax.set_title('By date')
            ax.set_ylabel("Count")
            ax.set_xlabel("Date")
            ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
            ax.yaxis.set_minor_locator(LinearLocator(25))

            
            # plt.show()
            print("got data")
                
            # except Exception as e:
            #     print(e)
            #     messages.error(request, f'Failed to fetch {series} from the FRED database.')
            # messages.success(request, f'Successfully fetched {series}.')

            flike = io.BytesIO()
            fig.savefig(flike)
            b64 = base64.b64encode(flike.getvalue()).decode()

            render(request, 'index.html', {'form': form, 'graph':b64})
    else:
        form = FREDForm()
    return render(request, 'index.html', {'form': form})