# Copyright (C) 2007-2009 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import threading
from SpiffSignal import Trackable

class Account(Trackable):
    """
    This class represents a user account.
    """

    def __init__(self, name, password, password2 = None, **kwargs):
        """
        Constructor.

        The authorization password is only required on hosts that
        separate the authentication from the authorization procedure.
        If an authorization password is not given, it defaults to the
        same value as the authentication password.

        @type  name: string
        @param name: A username.
        @type  password: string
        @param password: The authentication password.
        @type  password2: string
        @param password2: The authorization password, if required.
        @type  kwargs: dict
        @param kwargs: The following options are supported:
            - ssh_key_file: the key file that is used (SSH only).
        """
        Trackable.__init__(self)
        self.manager                = None
        self.name                   = name
        self.password               = password
        self.authorization_password = password2
        self.options                = kwargs
        self.lock                   = threading.Lock()


    def acquire(self):
        """
        Locks the account.
        """
        self.signal_emit('acquire_before', self)
        self.lock.acquire()
        self.signal_emit('acquired', self)


    def _acquire(self):
        """
        Like acquire(), but omits sending the signal.
        """
        self.lock.acquire()


    def release(self):
        """
        Unlocks the account.
        """
        self.signal_emit('release_before', self)
        self.lock.release()
        self.signal_emit('released', self)


    def get_name(self):
        """
        Returns the name of the account.

        @rtype:  string
        @return: The account name.
        """
        return self.name


    def get_password(self):
        """
        Returns the password of the account.

        @rtype:  string
        @return: The account password.
        """
        return self.password


    def get_authorization_password(self):
        """
        Returns the authorization password of the account.

        @rtype:  string
        @return: The account password.
        """
        return self.authorization_password or self.password