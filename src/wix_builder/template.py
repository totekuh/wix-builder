import uuid
from xml.sax.saxutils import escape as xml_escape

from .names import generate_name, random_version

EXE_WXS_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Name="{product_name}" Id="*"
           UpgradeCode="{product_guid}"
           Version="{version}" Manufacturer="{manufacturer}" Language="1033">
    <Package InstallerVersion="200" Compressed="yes" />
    <Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="{install_folder}"/>
      </Directory>
    </Directory>

    <Component Id="{component_id}" Guid="{component_guid}" Directory="INSTALLFOLDER">
      <File Id="{file_id}" Source="{exe_name}" KeyPath="yes" />
    </Component>

    <Feature Id="DefaultFeature" Title="{feature_title}" Level="1">
      <ComponentRef Id="{component_id}"/>
    </Feature>

    <CustomAction Id="{action_name}"
                  FileKey="{file_id}"
                  ExeCommand=""
                  Return="asyncNoWait"/>

    <InstallExecuteSequence>
      <Custom Action="{action_name}" After="InstallFinalize">1</Custom>
    </InstallExecuteSequence>
  </Product>
</Wix>
"""


CMD_WXS_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Name="{product_name}" Id="*"
           UpgradeCode="{product_guid}"
           Version="{version}" Manufacturer="{manufacturer}" Language="1033">
    <Package InstallerVersion="200" Compressed="yes" />
    <Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="{install_folder}"/>
      </Directory>
    </Directory>

    <Component Id="{component_id}" Guid="{component_guid}" Directory="INSTALLFOLDER">
      <CreateFolder/>
    </Component>

    <Feature Id="DefaultFeature" Title="{feature_title}" Level="1">
      <ComponentRef Id="{component_id}"/>
    </Feature>

    <CustomAction Id="{action_name}"
                  Directory="TARGETDIR"
                  ExeCommand="__COMMAND__"
                  Return="asyncNoWait"/>

    <InstallExecuteSequence>
      <Custom Action="{action_name}" After="InstallFinalize">1</Custom>
    </InstallExecuteSequence>
  </Product>
</Wix>
"""


def _common_fields():
    return dict(
        product_guid=uuid.uuid4(),
        component_guid=uuid.uuid4(),
        product_name=generate_name(),
        manufacturer=generate_name(),
        version=random_version(parts=4),
        install_folder=generate_name(),
        component_id=generate_name(),
        feature_title=generate_name(),
        action_name=generate_name(),
    )


def render_wxs(exe_name: str) -> str:
    fields = _common_fields()

    return EXE_WXS_TEMPLATE.format(
        **fields,
        file_id=generate_name(),
        exe_name=exe_name,
    )


def render_wxs_cmd(command: str) -> str:
    fields = _common_fields()

    xml = CMD_WXS_TEMPLATE.format(**fields)
    return xml.replace("__COMMAND__", xml_escape(command, {'"': "&quot;"}))
