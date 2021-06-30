from django.shortcuts import render
from .models import Bid, Sticker
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    num_bids=Bid.objects.all().count()
    num_bids_a=Bid.objects.all().filter(status='a').count()
    num_bids_w=Bid.objects.all().filter(status='w').count()
    num_bids_f=Bid.objects.all().filter(status='f').count()

    all_stickers = Sticker.objects.all().filter(status='v')

    if request.user.is_authenticated:
        if request.user.has_perm('system.delete_bid'):
            all_users = list()
            for user in User.objects.all():
                user_num_bids_a=Bid.objects.filter(maker=user).filter(status='a').count()
                user_num_bids_w=Bid.objects.filter(maker=user).filter(status='w').count()
                user_num_bids_f=Bid.objects.filter(maker=user).filter(status='f').count()
                user_num_bids=user_num_bids_a+user_num_bids_w+user_num_bids_f
                all_users.append((user.get_username(), user_num_bids, user_num_bids_a, user_num_bids_w, user_num_bids_f,))

            return render(
                        request,
                        'index.html',
                        context={'num_bids': num_bids,
                                 'num_bids_a': num_bids_a,
                                 'num_bids_w': num_bids_w,
                                 'num_bids_f': num_bids_f,
                                 'all_stickers': all_stickers,
                                 'all_users': all_users},
    )

        user_num_bids_a=Bid.objects.filter(maker=request.user).filter(status='a').count()
        user_num_bids_w=Bid.objects.filter(maker=request.user).filter(status='w').count()
        user_num_bids_f=Bid.objects.filter(maker=request.user).filter(status='f').count()
        user_num_bids=user_num_bids_a+user_num_bids_w+user_num_bids_f

        return render(
                        request,
                        'index.html',
                        context={'num_bids': num_bids,
                                 'num_bids_a': num_bids_a,
                                 'num_bids_w': num_bids_w,
                                 'num_bids_f': num_bids_f,
                                 'all_stickers': all_stickers,
                                 'user_num_bids': user_num_bids,
                                 'user_num_bids_a': user_num_bids_a,
                                 'user_num_bids_w': user_num_bids_w,
                                 'user_num_bids_f': user_num_bids_f},
    )

    return render(
        request,
        'index.html',
        context={'num_bids': num_bids,
                 'num_bids_a': num_bids_a,
                 'num_bids_w': num_bids_w,
                 'num_bids_f': num_bids_f,
                 'all_stickers': all_stickers},
    )


class BidListView(generic.ListView):
    model = Bid
    paginate_by = 25
    def get_queryset(self):
        return Bid.objects.all().exclude(status="f").order_by('-time_creation')
    # def get_queryset(self):
    #     if 'change' in self.request.GET:
    #         message = 'You searched for:'
    #     else:
    #         message = 'You submitted an empty form.'
    #     return HttpResponse(message)

class BidArchiveView(generic.ListView):
    model = Bid
    paginate_by = 25
    def get_queryset(self):
        return Bid.objects.all().filter(status="f").order_by('-time_creation')


class BidDetailView(generic.DetailView):
    model = Bid


class MakingBidsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Bid
    template_name ='system/bids_for_user.html'
    paginate_by = 10
    # login_url = '/login/'
    #     # redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Bid.objects.all().exclude(status="f").filter(maker=self.request.user).order_by('-time_creation')
        # return Bid.objects.all()


# class BidCreate(LoginRequiredMixin, CreateView):
#     model = Bid
#     fields = ['text', 'type_bid', 'location', 'telephone_num', 'bider', 'maker', 'helper']
#
#     permission_required = 'system.can_mark_returned'
#
#
#
#
# class BidUpdate(LoginRequiredMixin, UpdateView):
#     model = Bid
#     fields = ['text', 'type_bid', 'location', 'telephone_num', 'bider', 'maker', 'helper', 'comment', 'result', 'status']
#     permission_required = 'system.can_mark_returned'



class BidDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Bid
    success_url = reverse_lazy('bids')

    permission_required = ('system.delete_bid')



from system.forms import CreateBidForm


@login_required
def bid_create(request):
    """View function for renewing a specific BookInstance by librarian."""
    # book_instance = get_object_or_404(BookInstance, pk=pk)
    bid = Bid()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateBidForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            bid.text = form.cleaned_data['text']
            bid.type_bid = form.cleaned_data['type_bid']
            bid.location = form.cleaned_data['location']
            bid.telephone_num = form.cleaned_data['telephone_num']
            bid.bider = form.cleaned_data['bider']
            bid.maker = form.cleaned_data['maker']

            bid.creator = request.user.get_username()

            bid.helper = form.cleaned_data['helper']
            bid.status = form.cleaned_data['status']
            bid.result = form.cleaned_data['result']
            bid.comment = form.cleaned_data['comment']

            if bid.status == "w" and bid.time_creation is None:
                bid.time_start = datetime.datetime.today()
                bid.time_creation = datetime.datetime.today()
            elif bid.status == "w":
                bid.time_start = datetime.datetime.today()
            elif bid.status == "a":
                bid.time_creation = datetime.datetime.today()
            elif bid.status == "f" and bid.time_creation is None and bid.time_start is None:
                bid.time_start = datetime.datetime.today()
                bid.time_creation = datetime.datetime.today()
                bid.time_done = datetime.datetime.today()
            elif bid.status == "f" and bid.time_start is None:
                bid.time_start = datetime.datetime.today()
                bid.time_done = datetime.datetime.today()

            bid.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('bid-detail', args=(bid.pk,)))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_text = " "
        form = CreateBidForm(initial={'text': proposed_text})

    context = {
        'form': form,
        'bid-detail': bid,
    }

    return render(request, 'system/bid_create.html', context)


@login_required
def bid_update(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    bid = get_object_or_404(Bid, pk=pk)
    # bid = Bid()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateBidForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            bid.text = form.cleaned_data['text']
            bid.type_bid = form.cleaned_data['type_bid']
            bid.location = form.cleaned_data['location']
            bid.telephone_num = form.cleaned_data['telephone_num']
            bid.bider = form.cleaned_data['bider']
            bid.maker = form.cleaned_data['maker']
            bid.helper = form.cleaned_data['helper']
            # bid.status = form.cleaned_data['status']
            bid.result = form.cleaned_data['result']
            bid.comment = form.cleaned_data['comment']
            if bid.status != form.cleaned_data['status']:
                bid.status = form.cleaned_data['status']
                if bid.status == "w":
                    bid.time_start = datetime.datetime.today()
                elif bid.status == "f":
                # bid.time_start = datetime.datetime.today()
                    bid.time_done = datetime.datetime.today()
            bid.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('bid-detail', args=(bid.pk,)))

    # If this is a GET (or any other method) create the default form
    else:

        form = CreateBidForm(initial={
            'text': bid.text,
            'type_bid': bid.type_bid,
            'location': bid.location,
            'telephone_num': bid.telephone_num,
            'bider': bid.bider,
            'maker': bid.maker,
            'helper': bid.helper,
            'status': bid.status,
            'result': bid.result,
            'comment': bid.comment
        })

    context = {
        'form': form,
        'bid': bid,
    }

    return render(request, 'system/bid_update.html', context)


from system.forms import CreateStickerForm


@login_required
def sticker_create(request):
    """View function for renewing a specific BookInstance by librarian."""
    # book_instance = get_object_or_404(BookInstance, pk=pk)
    sticker = Sticker()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateStickerForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            sticker.text = form.cleaned_data['text']
            sticker.status = 'v'
            sticker.date_creation = datetime.datetime.today()

            sticker.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form
    else:
        # proposed_text = "Some text"
        form = CreateStickerForm()

    context = {
        'form': form,
        'sticker': sticker,
    }

    return render(request, 'system/sticker_create.html', context)


class StickerDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sticker
    success_url = reverse_lazy('index')
    permission_required = ('system.delete_sticker')


from system.forms import SearchForm


def bid_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Bid.objects.all().filter(id=query).order_by('-time_creation')
    return render(request,
                  'system/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
