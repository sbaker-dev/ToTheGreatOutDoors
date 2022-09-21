from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from ..models import TravelLocation, Comment, Favorite


class Place(View):
    """
    A given place has multiple ways of interacting with the page
    """

    @staticmethod
    def _initialise(place_name, place_location):
        """
        Get a unique location from TravelLocations by filtering on place_location, and then match the place_name,
        which is a raw name to strip out slashes that will otherwise break the view path, to the raw name of the isolated
        location.
        """
        location = TravelLocation.objects.filter(place=place_location)
        location = [place for place in location if place.raw_name() == place_name]

        # TODO: We clearly need to store / make a GID, as locations can share names within a district
        if len(location) > 1:
            print("Warning, found multiple locations within the same name in the same location!")
        location = location[0]
        comment_list = location.comment_set.all().order_by('-created')
        return location, comment_list

    def get(self, request, place_name, place_location):
        """
        Get the location and comment list for this page. Filter the base comments (made on the page) and replies,
        made in relation to some posting on that page, by checking the comment.comment_level.

        """
        # Load the current location and that locations comment list from the place_name and place_location
        location, comment_list = self._initialise(place_name, place_location)

        # Filter comments to be the base comments and replies on the comment_level.
        base_comments = [comment for comment in comment_list if comment.comment_level == 0]
        replies = [comment for comment in comment_list if comment.comment_level > 0]

        context = {'comment_list': base_comments, 'location': location, 'replies': replies,
                   'favourite': self._get_favourite(request, location)}
        return render(request, 'pages/place_details.html', context)

    @staticmethod
    def _get_favourite(request, location):
        """
        If the user is authenticated, then check to see if the user has this location in their favourites, otherwise
        false by definition
        """
        if request.user.is_authenticated:
            return len(Favorite.objects.filter(Q(user=request.user) & Q(location=location))) == 1
        else:
            return False

    def post(self, request, place_name, place_location):
        """
        A given Place is fairly interactive. We need to handle 3 explicit post requests of comment, favourite, and
        replies
        """
        # Load the current location and that locations comment list from the place_name and place_location
        location, comment_list = self._initialise(place_name, place_location)

        # Redirect to the page conditional on the POST type
        if 'comment' in request.POST:
            return self._post_comment(request, location, comment_list, place_name, place_location)

        elif 'favourite' in request.POST:
            return self._post_favourite(request, location, place_name, place_location)

        elif 'reply' in request.POST:
            return self._post_reply(request, place_name, place_location)

        else:
            print(f"WARNING: UNKNOWN POST COMMENT OF {request.POST} found and is unhandled within Place.post")

    @staticmethod
    def _post_comment(request, location, comment_list, place_name, place_location):
        """
        Add the request users comment to this locations comment list, assign its group ID as the length of current
        base comments, that way we can filter / style them seperatly
        """
        Comment.objects.create(user=request.user,
                               location=location,
                               body=request.POST.get('body'),
                               comment_group=len(comment_list))
        return redirect('place', place_name=place_name, place_location=place_location)

    @staticmethod
    def _post_favourite(request, location, place_name, place_location):
        """
        If the current location is not within the users Favourites, then we add it to their favourites. Else, if we
        can find the current favourite by filter on user, then we delete it.
        """
        # If it was a favourite, un-favourite it
        try:
            Favorite.objects.get(user=request.user, location=location).delete()
            return redirect('place', place_name=place_name, place_location=place_location)

        # Otherwise, add it as a fav
        except ObjectDoesNotExist:
            Favorite.objects.create(user=request.user, location=location)
            return redirect('place', place_name=place_name, place_location=place_location)

    @staticmethod
    def _post_reply(request, place_name, place_location):
        """
        If someone posts a reply, we need to also assign the parent comments ID, and it's group, for formatting. Replies
        have a comment level equal to the comment that was replied to + 1.
        """
        original_comment = Comment.objects.get(id=request.POST.get('id'))

        Comment.objects.create(user=request.user,
                               location=original_comment.location,
                               body=request.POST.get('body'),
                               comment_level=original_comment.comment_level + 1,
                               comment_group=original_comment.comment_group,
                               parent=original_comment.id)
        return redirect('place', place_name=place_name, place_location=place_location)