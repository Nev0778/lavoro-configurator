# Lavoro Configurator — WordPress Integration Guide

This guide explains how to embed the bespoke file download configurator into the Lavoro Design staging site (WordPress/WooCommerce).

## Option 1: Direct iframe Embed (Recommended)

The simplest and most robust way to add the configurator to a WooCommerce product page or standard WordPress page is via an iframe. This ensures the configurator's custom CSS and JavaScript do not conflict with your WordPress theme.

1. Open your WordPress admin dashboard and navigate to the **Product** or **Page** where you want the configurator.
2. Add a **Custom HTML** block (if using Gutenberg) or switch to the **Text** tab (if using the Classic Editor).
3. Paste the following code:

```html
<div style="position: relative; width: 100%; padding-bottom: 75%; height: 0; overflow: hidden; border: 1px solid #e2e0dc;">
  <iframe 
    src="https://lavoro-configurator.onrender.com" 
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
    allow="xr-spatial-tracking"
    title="Lavoro Advance Configurator">
  </iframe>
</div>
```

*Note: Replace the `src` URL with your final production URL once deployed. The `allow="xr-spatial-tracking"` attribute is required for the Augmented Reality feature to work on mobile devices.*

## Option 2: WooCommerce Product Tab Integration

If you want the configurator to appear as a dedicated tab alongside "Description" and "Reviews" on the WooCommerce product page, you can add a snippet to your theme's `functions.php` file.

1. Go to **Appearance > Theme File Editor** in your WordPress admin.
2. Select your child theme's `functions.php` file.
3. Add the following PHP snippet:

```php
add_filter( 'woocommerce_product_tabs', 'lavoro_add_configurator_tab' );

function lavoro_add_configurator_tab( $tabs ) {
    // Only add the tab for specific products (replace 123 with your product ID)
    global $product;
    if ( $product && $product->get_id() == 123 ) {
        $tabs['configurator_tab'] = array(
            'title'    => __( 'BIM & CAD Configurator', 'woocommerce' ),
            'priority' => 15,
            'callback' => 'lavoro_configurator_tab_content'
        );
    }
    return $tabs;
}

function lavoro_configurator_tab_content() {
    echo '<h2>Bespoke File Downloads</h2>';
    echo '<p>Configure your exact desk dimensions and finishes to instantly generate parametric BIM and CAD files.</p>';
    echo '<div style="position: relative; width: 100%; height: 800px; border: 1px solid #e2e0dc;">
            <iframe src="https://lavoro-configurator.onrender.com" style="width: 100%; height: 100%; border: 0;" allow="xr-spatial-tracking"></iframe>
          </div>';
}
```

## Option 3: Full Page Takeover Template

If you want the configurator to take up the entire page without the standard WordPress header and footer (ideal for a dedicated portal or sales tool), create a custom page template.

1. Create a file named `page-configurator.php` in your child theme folder.
2. Add the following code:

```php
<?php
/* Template Name: Full Screen Configurator */
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php wp_title(); ?></title>
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <iframe src="https://lavoro-configurator.onrender.com" allow="xr-spatial-tracking"></iframe>
</body>
</html>
```

3. In WordPress, create a new Page, set the Template to **Full Screen Configurator**, and publish.
