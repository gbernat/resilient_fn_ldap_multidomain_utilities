# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging
from resilient_circuits import ResilientComponent, function, handler, StatusMessage, FunctionResult, FunctionError
from fn_ldap_multidomain_utilities.util.helper import LDAPUtilitiesHelper
from ldap3 import MODIFY_REPLACE
from ast import literal_eval

PACKAGE_NAME = "fn_ldap_multidomain_utilities"


class FunctionComponent(ResilientComponent):
    """Component that implements Resilient function 'ldap_md_utilities_update''"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(FunctionComponent, self).__init__(opts)
        self.options = opts.get(PACKAGE_NAME, {})

    @handler("reload")
    def _reload(self, event, opts):
        """Configuration options have changed, save new values"""
        self.options = opts.get(PACKAGE_NAME, {})

    @function("ldap_md_utilities_update")
    def _ldap_md_utilities_update_function(self, event, *args, **kwargs):
        """Function: A function that updates the attribute of a DN with a new value"""
        try:

            # Get the wf_instance_id of the workflow this Function was called in
            wf_instance_id = event.message["workflow_instance"]["workflow_instance_id"]

            yield StatusMessage("Starting 'ldap_md_utilities_update' running in workflow '{0}'".format(wf_instance_id))

            # Get the function parameters:
            ldap_md_domain_name = kwargs.get("ldap_md_domain_name")  # text
            ldap_md_dn = kwargs.get("ldap_md_dn")  # text
            ldap_md_attribute_name = kwargs.get("ldap_md_attribute_name")  # text
            ldap_md_attribute_values = kwargs.get("ldap_md_attribute_values")  # text

            log = logging.getLogger(__name__)
            log.info("ldap_md_domain_name: %s", ldap_md_domain_name)
            log.info("ldap_md_dn: %s", ldap_md_dn)
            log.info("ldap_md_attribute_name: %s", ldap_md_attribute_name)
            log.info("ldap_md_attribute_values: %s", ldap_md_attribute_values)
            yield StatusMessage("Function Inputs OK")


            # Instansiate helper (which gets appconfigs from file)
            helper = LDAPUtilitiesHelper(self.options, ldap_md_domain_name)
            log.info("[app.config] -ldap_server: %s", helper.LDAP_SERVER)
            log.info("[app.config] -ldap_user_dn: %s", helper.LDAP_USER_DN)
            yield StatusMessage("Appconfig Settings OK")


            ##############################################

            try:
              # Try converting input to an array
              ldap_md_attribute_values = literal_eval(ldap_md_attribute_values)
            except Exception:
              raise ValueError("""ldap_md_attribute_values must be a string repersenation of an array e.g. "['stringValue1, 1234, 'stringValue2']" """)

            # Instansiate LDAP Server and Connection
            c = helper.get_ldap_connection()

            try:
              # Bind to the connection
              c.bind()
            except Exception as err:
              raise ValueError("Cannot connect to LDAP Server. Ensure credentials are correct\n Error: {0}".format(err))

            # Inform user
            msg = ""
            if helper.LDAP_IS_ACTIVE_DIRECTORY:
              msg = "Connected to {0}".format("Active Directory")
            else:
              msg = "Connected to {0}".format("LDAP Server")
            yield StatusMessage(msg)

            res = False
            try:
              yield StatusMessage("Attempting to update {0}".format(ldap_md_attribute_name))
              # perform the Modify operation
              # Prod: res = c.modify(ldap_md_dn, {ldap_md_attribute_name: [(MODIFY_REPLACE, ldap_md_attribute_values)]})
              # Test:
              res = 'c.modify(' + str(ldap_md_dn) + ', {' + str(ldap_md_attribute_name) + ': [(MODIFY_REPLACE, ' + str(ldap_md_attribute_values) + ')]})'

            except Exception:
              raise ValueError("Failed to update. Ensure 'ldap_md_dn' is valid and the update meets your LDAP CONSTRAINTS")
          
            finally:
              # Unbind connection
              c.unbind()

            ##############################################


            results = {
                "success": res,
                "domain_name": ldap_md_domain_name,
                "attribute_name": ldap_md_attribute_name,
                "attribute_values": ldap_md_attribute_values,
                "user_dn": ldap_md_dn                
            }

            yield StatusMessage("Finished 'ldap_md_utilities_update' that was running in workflow '{0}'".format(wf_instance_id))

            # Produce a FunctionResult with the results
            yield FunctionResult(results)
        except Exception:
            yield FunctionError()
