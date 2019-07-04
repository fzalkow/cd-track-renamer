import argparse
import urllib.parse
import requests
import os
from glob import glob
import shutil


def escape(s):
    return s.replace(':', '').replace('/', '-')


def get_albums(artist, album):
    url = 'http://musicbrainz.org/ws/2/release/?query=artist:{artist}%20AND%20release:{album}&fmt=json'.format(
        artist=urllib.parse.quote(artist), album=urllib.parse.quote(album))

    data = requests.get(url=url).json()

    return data['releases']


def get_tracks(release_id):
    url = 'http://musicbrainz.org/ws/2/release/{}?inc=recordings&fmt=json'.format(release_id)

    data = requests.get(url=url).json()

    titles = []
    num_cds = len(data['media'])

    for i, media in enumerate(data['media']):
        cur_titles = []
        for t, track in enumerate(media['tracks']):
            if num_cds == 1:
                cur_title = '{:02d} {}'.format(t+1, escape(track['title']))
            else:
                cur_title = '{:d}-{:02d} {}'.format(i+1, t+1, escape(track['title']))
            cur_titles.append(cur_title)
        titles.append(cur_titles)

    return titles


def eventually_rename_file(old_file, new_name, mode):
    new_fn = os.path.join(directory, new_name + os.path.splitext(old_file)[1])
    print('"{}" -> "{}"'.format(os.path.relpath(old_file, directory), os.path.relpath(new_fn, directory)))

    if mode == 'move':
        shutil.move(old_file, new_fn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Name Audio Files')
    parser.add_argument('--directory', required=True, help='album with audio files')
    parser.add_argument('--artist', required=True, help='name of artist')
    parser.add_argument('--album', required=True, help='name of album')
    parser.add_argument('--mode', default='test', help='test or move (default: test)')

    args = parser.parse_args()

    artist = args.artist
    album = args.album
    directory = args.directory
    mode = args.mode
    assert mode in ['test', 'move']

    # print candidate releases
    candidates = get_albums(artist, album)

    for i, candidate in enumerate(candidates):
        country = candidate['country'] if 'country' in candidate else 'Unknown country'
        num_cds = len(candidate['media'])
        cd_s = 's' if num_cds > 1 else ''

        print('{n:2d} - {artist}: {title} ({country}, {ncds} CD{cd_s}, {ntracks} tracks)'.format(
              n=i+1, title=candidate['title'],
              artist=' / '.join([a['artist']['name'] for a in candidate['artist-credit']]),
              ntracks=candidate['track-count'], country=country, ncds=num_cds, cd_s=cd_s))

    # user chooses among candidate releases
    candidate_no = input('Which album number do you want to use? ')
    candidate_idx = (int(candidate_no) - 1)
    release_id = candidates[candidate_idx]['id']

    # get tracks from chosen candidate release
    track_names = get_tracks(release_id)

    # rename files / print potential renaming
    directory_content = sorted(glob(os.path.join(directory, '*')))
    directory_files = [f for f in directory_content if os.path.isfile(f)]
    directory_subdirs = [f for f in directory_content if os.path.isdir(f)]
    directory_subdir_files = [sorted(glob(os.path.join(d, '*'))) for d in directory_subdirs]

    # single cd
    if len(track_names) == 1:
        assert len(track_names[0]) == len(directory_files)

        for fn, name in zip(directory_files, track_names[0]):
            eventually_rename_file(fn, name, mode)

    # multiple cds
    else:
        assert len(track_names) == len(directory_subdirs)
        assert all(len(t) == len(d) for t, d in zip(track_names, directory_subdir_files))

        for cur_names, cur_files in zip(track_names, directory_subdir_files):
            for fn, name in zip(cur_files, cur_names):
                eventually_rename_file(fn, name, mode)
