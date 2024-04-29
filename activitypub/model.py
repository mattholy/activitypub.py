import mimetypes
import isodate
from babel.core import Locale, UnknownLocaleError
import pycountry

from pydantic import BaseModel, Field, HttpUrl
from pydantic import field_validator
from datetime import datetime
from typing import Optional, Union, List, Dict, Any, Literal


# ActivityPub Type
mimetypes.add_type(
    'application/ld+json; profile="https://www.w3.org/ns/activitystreams"', '.json')
mimetypes.add_type('application/activity+json', '.json')


class ActivityStreamsBase(BaseModel):
    activitypub_context: Optional[
        Union[HttpUrl, List[Union[HttpUrl, Dict[str, Any]]]]
    ] = Field(None, alias='@context')
    id: Optional[HttpUrl] = Field(None, alias='id')
    type: Optional[str] = Field(None, alias='type')

    @field_validator('activitypub_context')
    def validate_context(cls, value):
        if (
            isinstance(value, str)
            and 'https://www.w3.org/ns/activitystreams' not in value
        ):
            raise ValueError(
                '@context must include "https: // www.w3.org/ns/activitystreams".'
            )
        if (
            isinstance(value, list)
            and 'https://www.w3.org/ns/activitystreams' not in value
        ):
            raise ValueError(
                '@context must include "https: // www.w3.org/ns/activitystreams".'
            )
        return value

    class Config:
        populate_by_name = True


class BaseObject(ActivityStreamsBase):
    type: str = Field(None, alias='type')

    attachment: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                               List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='attachment')
    attributed_to: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                                  List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='attributedTo')
    audience: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                             List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='audience')
    content: Optional[str] = Field(None, alias='content')
    content_map: Optional[Dict[str, str]] = Field(None, alias='contentMap')
    context: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                            List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='context')
    name: Optional[str] = Field(None, alias='name')
    name_map: Optional[Dict[str, str]] = Field(None, alias='nameMap')
    end_time: Optional[datetime] = Field(None, alias='endTime')
    generator: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                              List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='generator')
    icon: Optional[Union[HttpUrl, 'ImageObject', 'BaseLink',
                         List[Union[HttpUrl, 'ImageObject', 'BaseLink']]]] = Field(None, alias='icon')
    image: Optional[Union['ImageObject', List['ImageObject']]
                    ] = Field(None, alias='image')
    in_reply_to: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                                List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='inReplyTo')
    location: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                             List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='location')
    preview: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                            List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='preview')
    published: Optional[datetime] = Field(None, alias='published')
    replies: Optional['BaseCollection'] = Field(None, alias='replies')
    start_time: Optional[datetime] = Field(None, alias='startTime')
    summary: Optional[str] = Field(None, alias='summary')
    summary_map: Optional[Dict[str, str]] = Field(None, alias='summaryMap')
    tag: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                        List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='tag')
    updated: Optional[datetime] = Field(None, alias='updated')
    url: Optional[Union[HttpUrl, 'BaseLink',
                        List[Union[HttpUrl, 'BaseLink']]]] = Field(None, alias='url')
    to: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                       List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='to')
    bto: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                        List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='bto')
    cc: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                       List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='cc')
    bcc: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                        List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='bcc')
    media_type: Optional[str] = Field(None, alias='mediaType')
    duration: Optional[str] = Field(None, alias='duration')

    @field_validator('media_type')
    def check_media_type(cls, value):
        extension = mimetypes.guess_extension(value)
        if not extension:
            raise ValueError(f"Invalid MIME type: {value}")
        return value

    @field_validator('duration')
    def validate_duration(cls, v):
        try:
            parsed_duration = isodate.parse_duration(v)
            return v
        except (isodate.ISO8601Error, ValueError):
            raise ValueError(f"Invalid XSD duration format: {v}")

    @field_validator('content_map')
    def validate_language_codes(cls, v):
        if v is not None:
            for lang in v.keys():
                try:
                    Locale.parse(lang, sep='-')
                except UnknownLocaleError:
                    raise ValueError(
                        f"Invalid ISO language code in contentMap: {lang}")
        return v

    @field_validator('name_map')
    def validate_language_codes(cls, v):
        if v is not None:
            for lang in v.keys():
                try:
                    Locale.parse(lang, sep='-')
                except UnknownLocaleError:
                    raise ValueError(
                        f"Invalid ISO language code in nameMap: {lang}")
        return v

    @field_validator('summary_map')
    def validate_language_codes(cls, v):
        if v is not None:
            for lang in v.keys():
                try:
                    Locale.parse(lang, sep='-')
                except UnknownLocaleError:
                    raise ValueError(
                        f"Invalid ISO language code in summaryMap: {lang}")
        return v


class BaseLink(ActivityStreamsBase):
    href: HttpUrl = Field(None, alias='href')
    rel: Optional[str] = Field(None, alias='rel')
    media_type: Optional[str] = Field(None, alias='mediaType')
    name: Optional[str] = Field(None, alias='name')
    name_map: Optional[Dict[str, str]] = Field(None, alias='nameMap')
    hreflang: Optional[str] = Field(None, alias='hreflang')
    height: Optional[int] = Field(None, alias='height', ge=0)
    width: Optional[int] = Field(None, alias='width', ge=0)
    preview: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                            List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='preview')

    @field_validator('name_map')
    def validate_language_codes(cls, v):
        if v is not None:
            for lang in v.keys():
                try:
                    Locale.parse(lang, sep='-')
                except UnknownLocaleError:
                    raise ValueError(
                        f"Invalid ISO language code in nameMap: {lang}")
        return v

    @field_validator('rel')
    def check_link_relation(cls, v):
        invalid_chars = " \t\n\f\r,"
        if any(char in invalid_chars for char in v):
            raise ValueError(
                f"Link relation contains invalid characters. Valid characters should not include any of: {invalid_chars}")
        return v

    @field_validator('hreflang')
    def validate_bcp47_language_tag(cls, v):
        try:
            if pycountry.languages.lookup(v):
                return v
        except LookupError:
            raise ValueError(f"Invalid BCP47 language tag: {v}")


class BaseActivity(BaseObject):
    type: Literal[
        'Accept', 'Add', 'Announce', 'Arrive', 'Block', 'Create', 'Delete',
        'Dislike', 'Flag', 'Follow', 'Ignore', 'Invite', 'Join', 'Leave',
        'Like', 'Listen', 'Move', 'Offer', 'Question', 'Reject', 'Read',
        'Remove', 'TentativeReject', 'TentativeAccept', 'Travel', 'Undo',
        'Update', 'View'
    ] = Field(None, alias='type')
    actor: Optional[Union[HttpUrl, 'Actor', 'BaseLink',
                          List[Union[HttpUrl, 'Actor', 'BaseLink']]]] = Field(None, alias='actor')
    object: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                           List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='object')
    target: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                           List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='target')
    result: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                           List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='result')
    origin: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                           List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='origin')
    instrument: Optional[Union[HttpUrl, 'BaseObject', 'BaseLink',
                               List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(None, alias='instrument')


class IntransitiveActivity(BaseActivity):
    object: None = Field(None, alias='object')


class BaseCollection(BaseObject):
    type: str = 'Collection'
    total_items: Optional[int] = Field(None, alias='totalItems', ge=0)
    current: Optional[Union[HttpUrl, 'CollectionPage', 'BaseLink',
                            List[Union[HttpUrl, 'CollectionPage', 'BaseLink']]]] = Field(None, alias='current')
    first: Optional[Union[HttpUrl, 'CollectionPage', 'BaseLink',
                          List[Union[HttpUrl, 'CollectionPage', 'BaseLink']]]] = Field(None, alias='first')
    last: Optional[Union[HttpUrl, 'CollectionPage', 'BaseLink',
                         List[Union[HttpUrl, 'CollectionPage', 'BaseLink']]]] = Field(None, alias='last')
    items: Optional[Union[List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(
        None, alias='items')
    ordered_items: Optional[Union[List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(
        None, alias='orderedItems')


class OrderedCollection(BaseCollection):
    type: str = 'OrderedCollection'


class CollectionPage(BaseCollection):
    type: str = 'CollectionPage'
    part_of: Optional[Union[HttpUrl, BaseCollection]
                      ] = Field(None, alias='partOf')
    next: Optional[Union[HttpUrl, BaseCollection]] = Field(None, alias='next')
    prev: Optional[Union[HttpUrl, BaseCollection]] = Field(None, alias='prev')


class OrderedCollectionPage(CollectionPage):
    type: str = 'OrderedCollectionPage'
    start_index: Optional[int] = Field(None, alias='startIndex', ge=0)


class Actor(ActivityStreamsBase):
    type: str = Field(None, alias='type')
    inbox: HttpUrl = Field(None, alias='inbox')
    outbox: HttpUrl = Field(None, alias='outbox')
    following: Optional[HttpUrl] = Field(None, alias='following')
    followers: Optional[HttpUrl] = Field(None, alias='followers')
    liked: Optional[HttpUrl] = Field(None, alias='liked')
    streams: Optional[List[HttpUrl]] = Field(None, alias='streams')
    preferred_username: Optional[str] = Field(None, alias='preferredUsername')
    endpoints: Optional[Dict[str, HttpUrl]] = Field(None, alias='endpoints')
    proxy_url: Optional[HttpUrl] = Field(None, alias='proxyUrl')
    oauth_authorization_endpoint: Optional[HttpUrl] = Field(
        None, alias='oauthAuthorizationEndpoint')
    oauth_token_endpoint: Optional[HttpUrl] = Field(
        None, alias='oauthTokenEndpoint')
    provide_client_key: Optional[HttpUrl] = Field(
        None, alias='provideClientKey')
    sign_client_key: Optional[HttpUrl] = Field(None, alias='signClientKey')
    shared_inbox: Optional[HttpUrl] = Field(None, alias='sharedInbox')

# =================================================================================================
# Activity Types
# =================================================================================================


class AcceptActivity(BaseActivity):
    type: str = Field('Accept')


class AddActivity(BaseActivity):
    type: str = Field('Add')


class AnnounceActivity(BaseActivity):
    type: str = Field('Announce')


class ArriveActivity(IntransitiveActivity):
    type: str = Field('Arrive')


class CreateActivity(BaseActivity):
    type: str = Field('Create')


class DeleteActivity(BaseActivity):
    type: str = Field('Delete')


class DislikeActivity(BaseActivity):
    type: str = Field('Dislike')


class FlagActivity(BaseActivity):
    type: str = Field('Flag')


class FollowActivity(BaseActivity):
    type: str = Field('Follow')


class IgnoreActivity(BaseActivity):
    type: str = Field('Ignore')


class BlockActivity(IgnoreActivity):
    type: str = Field('Block')


class JoinActivity(BaseActivity):
    type: str = Field('Join')


class LeaveActivity(BaseActivity):
    type: str = Field('Leave')


class LikeActivity(BaseActivity):
    type: str = Field('Like')


class ListenActivity(BaseActivity):
    type: str = Field('Listen')


class MoveActivity(BaseActivity):
    type: str = Field('Move')


class OfferActivity(BaseActivity):
    type: str = Field('Offer')


class InviteActivity(OfferActivity):
    type: str = Field('Invite')


class QuestionActivity(IntransitiveActivity):
    type: str = Field('Question')
    one_of: Optional[Union[List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(
        None, alias='oneOf')
    any_of: Optional[Union[List[Union[HttpUrl, 'BaseObject', 'BaseLink']]]] = Field(
        None, alias='anyOf')
    closed: Optional[Union[datetime, bool, BaseObject,
                           BaseLink, HttpUrl]] = Field(None, alias='closed')


class RejectActivity(BaseActivity):
    type: str = Field('Reject')


class ReadActivity(BaseActivity):
    type: str = Field('Read')


class RemoveActivity(BaseActivity):
    type: str = Field('Remove')


class TentativeRejectActivity(RejectActivity):
    type: str = Field('TentativeReject')


class TentativeAcceptActivity(AcceptActivity):
    type: str = Field('TentativeAccept')


class TravelActivity(IntransitiveActivity):
    type: str = Field('Travel')


class UndoActivity(BaseActivity):
    type: str = Field('Undo')


class UpdateActivity(BaseActivity):
    type: str = Field('Update')


class ViewActivity(BaseActivity):
    type: str = Field('View')

# =================================================================================================
# Actor Types
# =================================================================================================


class ApplicationActor(Actor):
    type: str = Field('Application')


class GroupActor(Actor):
    type: str = Field('Group')


class OrganizationActor(Actor):
    type: str = Field('Organization')


class PersonActor(Actor):
    type: str = Field('Person')


class ServiceActor(Actor):
    type: str = Field('Service')

# =================================================================================================
# Object Types
# =================================================================================================


class ArticleObject(BaseObject):
    type: str = Field('Article')


class DocumentObject(BaseObject):
    type: str = Field('Document')


class AudioObject(DocumentObject):
    type: str = Field('Audio')


class EventObject(BaseObject):
    type: str = Field('Event')


class ImageObject(DocumentObject):
    type: str = Field('Image')


class NoteObject(BaseObject):
    type: str = Field('Note')


class PageObject(DocumentObject):
    type: str = Field('Page')


class PlaceObject(BaseObject):
    type: str = Field('Place')
    accuracy: Optional[float] = Field(None, alias='accuracy', ge=0, le=100)
    altitude: Optional[float] = Field(None, alias='altitude')
    latitude: Optional[float] = Field(None, alias='latitude')
    longitude: Optional[float] = Field(None, alias='longitude')
    radius: Optional[float] = Field(None, alias='radius', ge=0)
    units: Union[HttpUrl, Literal['cm', 'feet', 'inches',
                                  'km', 'm', 'miles']] = Field('m', alias='units')


class ProfileObject(BaseObject):
    type: str = Field('Profile')


class RelationshipObject(BaseObject):
    type: str = Field('Relationship')
    subject: Union[HttpUrl, BaseObject] = Field(None, alias='subject')
    object: Union[HttpUrl, BaseObject] = Field(None, alias='object')
    relationship: Optional[str] = Field(None, alias='relationship')


class TombstoneObject(BaseObject):
    type: str = Field('Tombstone')
    former_type: str = Field(None, alias='formerType')
    deleted: datetime = Field(None, alias='deleted')

    @field_validator('former_type')
    def check_media_type(cls, value):
        extension = mimetypes.guess_extension(value)
        if not extension:
            raise ValueError(f"Invalid MIME type: {value}")
        return value


class VideoObject(DocumentObject):
    type: str = Field('Video')

# =================================================================================================
# Link Types
# =================================================================================================


class MentionLink(BaseLink):
    type: str = Field('Mention')
